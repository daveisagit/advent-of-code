"""Number theory stuff"""


from itertools import combinations
import math


def extended_euclid(a: int, b: int):
    """Returns the Bézout coefficients s,t where
    as+bt=GCD"""
    prv_r, r = a, b
    prv_s, s = 1, 0
    prv_t, t = 0, 1
    while r != 0:
        q = prv_r // r
        prv_r, r = r, prv_r - q * r
        prv_s, s = s, prv_s - q * s
        prv_t, t = t, prv_t - q * t
    return prv_s, prv_t


def test_extended_euclid():
    """Test extended Euclid"""
    a, b = 11, 7
    s, t = extended_euclid(a, b)
    assert (s, t) == (2, -3)
    assert a * s + b * t == 1

    a, b = 7, 11
    s, t = extended_euclid(a, b)
    assert (s, t) == (-3, 2)
    assert a * s + b * t == 1

    a, b = 10, 15
    s, t = extended_euclid(a, b)
    assert (s, t) == (-1, 1)
    assert a * s + b * t == 5


def mod_inv(m, n):
    """Return the inverse of n in mod m
    Assuming (m,n) = 1, there exists s,t
    ms + nt = 1
    nt ≡ 1    (mod m)
    so t ≡ n' (mod m)
    """
    _, t = extended_euclid(m, n)
    return t % m


def solve_congruences(congruences: list) -> int:
    """Given a list of congruence equations expressed as triples.
    Check the moduli are all pairwise coprime

    X ≡ A1 (mod M1)
    ...
    X ≡ Ai (mod Mi)
    (A1,M1) , ... , (Ai,Mi)
    Return X ≡ LCM
    """
    # classes = [c[0] for c in congruences]
    moduli = [c[1] for c in congruences]
    chk = max(math.gcd(a, b) for a, b in combinations(moduli, 2))
    if chk != 1:
        raise ValueError("Moduli should be pairwise coprime")

    lcm = math.lcm(*moduli)
    total_cc = 0
    for a, m in congruences:
        other_moduli = [o for o in moduli if o != m]
        other_moduli_product = math.prod(other_moduli)
        inv = mod_inv(m, other_moduli_product)
        cc = a * other_moduli_product * inv
        total_cc += cc

    return total_cc % lcm
