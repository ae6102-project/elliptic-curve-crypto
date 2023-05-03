import numpy as np
from numba import njit
maxInt = np.uint32(4294967295)


def int2numpy(pyint):
    lim = 2**32
    arr = np.zeros((32,), dtype='uint32')
    rem = pyint
    index = 0
    while rem > 0:
        x = divmod(rem, lim)
        rem = x[0]
        arr[index] = x[1]
        index += 1
    return arr


def numpy2int(arr):
    temp = np.flip(arr)
    pyint = int(0)
    for i in range(31):
        pyint = (pyint + int(temp[i])) * int(2**32)
    return pyint+int(temp[31])


@njit
def add(x, y, res):
    carry = 0
    for i in range(32):
        res[i] = x[i]+carry
        carry = (res[i] < x[i])
        res[i] = y[i]+res[i]
        carry = (res[i] < y[i] or carry)


@njit
def subtract(x, y, res):
    borrow = 0
    for i in range(32):
        if (borrow == 0 or x[i] > 0) and x[i]-borrow >= y[i]:
            res[i] = (x[i]-borrow)-y[i]
            borrow = 0
        else:
            res[i] = x[i]+(maxInt-y[i])+(1-borrow)
            borrow = 1
    return borrow

# partial products


@njit
def pp(i, x, y, p):
    c = np.uint32(0)
    for j in range(32-i):
        temp = np.uint64(x[i])*y[j]
        p[i+j] = c+temp
        c = temp >> 32

# multiply (uses pp and add)


@njit
def multiply(x, y, res):
    temp = np.zeros((32,), 'uint32')
    for i in range(31):
        p = np.zeros((32,), 'uint32')
        pp(i, x, y, p)
        add(temp, p, res)
        temp = res.copy()

        
@njit
def divmod_single_word(x, y):
    scale = 1
    while y * scale <= x:
        scale <<= 1

    quotient = 0
    remainder = x
    
    while scale > 0:
        q = remainder // (y * scale)
        quotient += q * scale
        remainder -= q * y * scale
        scale >>= 1
        
    return quotient, remainder


@njit
def ndivmod(x,y,q,r):
    rpass = np.zeros_like(x)
    qpass = np.zeros_like(x)
    temp = np.zeros_like(x)
    zero = np.zeros_like(x)

    i = len(x)-1
    j = len(y)-1
    while True:
        if x[i]!=0 or i==0:
            break
        i -= 1
    while True:
        if y[j]!=0 or j==0:
            break
        j -= 1

    borrow = subtract(x, y, rpass)
    add(zero,x,r)
    add(zero,zero,q)

    while borrow == 0:
        while True:
            if r[i]!=0 or i==0:
                break
            i -= 1
    
        if i == j:
            qpass[0] = r[i]//y[j]
            multiply(y, qpass, temp)
            borrow = subtract(r, temp, rpass)

        elif i > j:
            qpass[i-j] = 1
            qpass[0] = r[i]//y[j]
            multiply(qpass, y, temp)
            borrow = subtract(r, temp, rpass)
            if borrow == 1:
                id = 32
                qpass[i-j] = 0
            while borrow == 1 and id>0:
                id -= 1
                qpass[i-j-1] = 1<<id
                multiply(qpass, y, temp)
                borrow = subtract(r, temp, rpass)

        add(zero,q,temp)
        add(temp,qpass,q)
        add(zero,rpass,r)
        add(zero,zero,qpass)

        borrow = subtract(r, y, rpass)


# Usage example
# x = 2**500
# a = int2numpy(x)
# b = int2numpy(x)
# c = int2numpy(0)

# multiply(a,b,c)
# print(numpy2int(c))

# x1 = np.zeros((32,), dtype='uint32')
# y1 = np.zeros((32,), dtype='uint32')
# q = np.zeros((32,), dtype='uint32')
# r = np.zeros((32,), dtype='uint32')
# ndivmod(x1,int2numpy(1),q,r)

# a = (778187298998769879879787979889573673298739781862586287182176178628769879424242323799)
# b = (42890007657567798765765757781767816837509721687275009)
# x1 = int2numpy(a)
# y1 = int2numpy(b)

# ndivmod(x1, y1, q, r)
# print((numpy2int(q),numpy2int(r)))
# print(divmod(a,b))
