import numpy as np
from numba import njit
maxInt = np.uint32(4294967295)

def int2numpy(pyint):
    lim = 2**32
    arr = np.zeros((32,), dtype='uint32')
    rem = pyint
    index = 0
    while rem>0:
        x = divmod(rem,lim)
        rem = x[0]
        arr[index] = x[1]
        index += 1
    return arr

def numpy2int(arr):
    multiplier = int(2**992)
    pyint = multiplier*arr[31]
    for i in range(31):
        multiplier = int(multiplier/2**32)
        pyint = pyint + multiplier*arr[30-i]
    return pyint

@njit
def add(x, y, res):
    carry = 0
    for i in range(32):
        res[i] = x[i]+carry
        carry = (res[i]<x[i])
        res[i] = y[i]+res[i]
        carry = (res[i]<y[i] or carry)

@njit
def subtract(x, y, res):
    borrow = 0
    for i in range(32):
        if (borrow==0 or x[i]>0) and x[i]-borrow>=y[i]:
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
        c = temp>>32

# multiply (uses pp and add)
@njit
def multiply(x, y, res):
    temp = np.zeros((32,),'uint32')
    for i in range(31):
        p = np.zeros((32,),'uint32')
        pp(i,x,y,p)
        add(temp,p,res)
        temp = res.copy()

#Usage example
x = 2**500
a = int2numpy(x)
b = int2numpy(x)
c = int2numpy(0)

multiply(a,b,c)
print(numpy2int(c))