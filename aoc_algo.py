import numpy as np


def chinese_remainder_theorem(remainders, moduli):
    """Find solution to system of modulus equations

        x == r1 (mod m1)
        x == r2 (mod m2)
        ...
        x == rN (mod mN)
    
    Input
        remainders: [r1, r2, ... rN]
        moduli:     [m1, m2, ... mN]
    """

    # For computational efficiency, sort on moduli
    moduli, remainders = tuple(zip(*sorted(zip(moduli, remainders), reverse=True)))

    M = moduli[0]
    x = remainders[0] % M
    for r, m in zip(remainders[1:], moduli[1:]):
        assert np.gcd(m, M) == 1, 'No common prime factors allowed among moduli'
        # Solve "x + q*N == r"
        #   q*N == r - x (mod m)
        #   q = (r-x (mod m)) * (N^-1 (mod m))
        q = ((r - x) % m) * pow(M, -1, m)

        # Adding q * M preserves previous remainders, while
        # introducing remainder r at current modulus m
        x += q * M
        M *= m
        x = x % M

    return x


