# Finding inverses of a number of a number modulo p
def inverse_dumb(a, p):
    for i in range(1, p):
        if a*i % p == 1:
            return i
    return -1

# Extended Euclid's Alogrithm O(log ap)


def inverse_euclid(a, p):
    gcd, x, y = euclid_gcd(a, p)
    if x < 0:
        x += p
    return x


def euclid_gcd(a, b):
    s = 0
    old_s = 1
    t = 1
    old_t = 0
    r = b
    old_r = a

    while r != 0:
        quotient = old_r//r
        old_r, r = r, old_r - quotient*r
        old_s, s = s, old_s - quotient*s
        old_t, t = t, old_t - quotient*t

    return [old_r, old_s, old_t]

# Fast Power Algorithm (Fermat)


def inverse_fermat(a, p):
    return fast_power(a, p-2, p)


def fast_power(base, power, MOD):
    result = 1
    while power > 0:
        if power % 2 == 1:
            result = (result * base) % MOD

        power = power // 2
        base = (base * base) % MOD
    return result
