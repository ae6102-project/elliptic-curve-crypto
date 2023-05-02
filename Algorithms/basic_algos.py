import numpy as np
from multiplicative_inverse import *


def bits(n):
    while n:
        yield n & 1
        n >>= 1


def doubleP(P):
    if P is None:
        return (None, None)
    x, y = P
    m = (3*x*x+a) * inverse_euclid(2*y, p) % p
    x1 = m*m - 2*x
    y1 = m*(x-x1) - y
    return (x1 % p, y1 % p)


def AddPQ(P, Q):
    if P is None or Q is None:  # check for the zero point
        return P or Q
    xp, yp = P
    xq, yq = Q
    if xp == xq:
        return doubleP(P)
    m = (yq-yp) * inverse_euclid((xq-xp), p) % p
    xr = m*m - xp - xq
    yr = m*(xp-xr) - yp
    return (xr % p, yr % p)


def DoubleAndAdd(k, P):
    Q = None
    ymp = P
    for b in bits(k):
        if b:
            Q = AddPQ(Q, tmp)
        tmp = doubleP(tmp)
    return Q

# Recursive Double and Add


def recursive_DnA(P, d):
    if(d == 0):
        return 0
    elif (d == 1):
        return P
    elif(d % 2 == 1):
        return AddPQ(P, recursive_DnA(P, d - 1))
    else:
        return recursive_DnA(doubleP(P), d / 2)


def MontgomeryLadder(k, P):
    bin_k = bin(k)[2:]
    l = len(bin_k)
    R0 = P
    R1 = doubleP(P)
    for i in range(l-2, -1, -1):
        if(bin_k[i] == '1'):
            R1 = AddPQ(R0, R1)
            R0 = doubleP(R0)
        else:
            R0 = AddPQ(R0, R1)
            R1 = doubleP(R1)
    return R0


def JoyesDoubleandAdd(k, P):
    bin_k = bin(k)[2:]
    l = len(bin_k)
    R0 = (0, 0)
    R1 = P
    for j in range(0, l):
        b = 1 - int(bin_k[j])
        if(b == 1):
            R1 = AddPQ(doubleP(R1), R0)
        else:
            R0 = AddPQ(doubleP(R0), R1)
    return R0
