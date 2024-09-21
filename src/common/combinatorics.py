"""Useful combinatorial stuff"""

from itertools import product
from common.numty import factors, phi


def necklace_arrangements_k_colours(n, k):
    """Only rotational symmetry considered: Cn"""
    fs = factors(n)
    r = 0
    for d in fs:
        r += phi(d) * (k ** (n // d))
    return r // n


# assert necklace_arrangements_k_colours(12, 2) == 352


def bracelet_arrangements_k_colours(n, k):
    """Dihedral symmetry: Dn"""

    na = necklace_arrangements_k_colours(n, k)

    # an adjustment for the reflections
    if n % 2 == 1:
        a = (k ** ((n + 1) // 2)) // 2
    else:
        a = (k ** (n // 2 + 1) + k ** (n // 2)) // 4

    return na // 2 + a


# assert bracelet_arrangements_k_colours(12, 2) == 224

# for poly circle take off 1+1+6 for the 0,1,2-gon to give 216
# = 1+1+6 (for 10,11,12-gon) + (12+29+38) x 2 + 50 (6gon)
# 3,4,5gon = 12+29+38 = 7,8,9gon


def cube_colourings(k):
    """Ways to colour faces of a cube in k colours"""
    return (k**6 + 3 * k**4 + 12 * k**3 + 8 * k**2) // 24


# assert cube_colourings(3) == 57


def generate_necklaces(n, k, bracelet=False):
    """Generator for n beads in k colours"""
    ranges = [range(k) for _ in range(n)]
    discovered = set()
    for x in product(*ranges):

        if x in discovered:
            continue

        for i in range(n):
            t = x[i:] + x[:i]
            discovered.add(t)
            if bracelet:
                r = t[::-1]
                discovered.add(r)

        yield x


# assert len(list(generate_necklaces(12, 2))) == 352
# assert len(list(generate_necklaces(12, 2, bracelet=True))) == 224
