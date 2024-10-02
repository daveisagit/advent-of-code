"""Number theory stuff"""

from collections import Counter
from functools import lru_cache, reduce
from itertools import combinations, islice, pairwise, product
from math import comb, lcm, prod, sqrt, gcd
from sys import getrecursionlimit, setrecursionlimit


def generate_rationals():
    """Return p,q such 0 < p < q and (p,q)=1"""
    q = 2
    while True:
        for p in range(1, q):
            if gcd(p, q) == 1:
                yield p, q
        q += 1


def generate_pythagorean_triples():
    """Return p,q such 0 < p < q and (p,q)=1"""
    for p, q in generate_rationals():
        x = q**2 - p**2
        y = 2 * p * q
        if gcd(x, y) != 1:
            continue
        z = q**2 + p**2
        yield min(x, y), max(x, y), z


def generate_pythagorean_triples_under(n):
    """All triple values are < n"""
    for t in generate_pythagorean_triples():
        if t[0] >= n:
            break
        if any(x >= n for x in t):
            continue
        yield t


def integer_root(n: int, e: int):
    """Returns the e-root of n if it is an integer"""
    r = int(n ** (1 / e))
    r_e = r**e
    if r_e == n:
        return r

    if r_e > n:
        r -= 1
        r_e = r**e

    while r_e < n:
        r += 1
        r_e = r**e
        if r_e == n:
            return r

    return None


def prime_list(n):
    """Return all the primes up to n
    PREFER list_of_primes()"""
    if n <= 2:
        return []
    sieve = [True] * (n + 1)
    for x in range(3, int(n**0.5) + 1, 2):
        for y in range(3, (n // x) + 1, 2):
            sieve[(x * y)] = False

    return [2] + [i for i in range(3, n, 2) if sieve[i]]


# or if generating primes with no limit


def generate_primes():
    """Generate an infinite sequence of prime numbers."""
    # Maps composites to primes witnessing their compositeness.
    # This is memory efficient, as the sieve is not "run forward"
    # indefinitely, but only as long as required by the current
    # number being tested.
    #
    D = {}

    # The running integer that's checked for primeness
    q = 2

    while True:
        if q not in D:
            # q is a new prime.
            # Yield it and mark its first multiple that isn't
            # already marked in previous iterations
            #
            yield q
            D[q * q] = [q]
        else:
            # q is composite. D[q] is the list of primes that
            # divide it. Since we've reached q, we no longer
            # need it in the map, but we'll mark the next
            # multiples of its witnesses to prepare for larger
            # numbers
            #
            for p in D[q]:
                D.setdefault(p + q, []).append(p)
            del D[q]

        q += 1


# for x in generate_primes():
#     print(x)
#     if x > 100:
#         break

# l = list(islice(generate_primes(), 50))
# print(l)


def list_of_primes(n):
    """Return all the primes <= n as a list"""
    l = []
    for p in generate_primes():
        if p > n:
            break
        l.append(p)
    return l


# def phi_safe(n):
#     """Euler's totient function
#     The number positive integers up to n
#     that are relatively prime to n"""
#     amount = 0
#     for k in range(1, n + 1):
#         if gcd(n, k) == 1:
#             amount += 1
#     return amount


def prime_factors(n):
    """Return all the prime factors of n
    360: [2, 2, 2, 3, 3, 5]"""
    primes = list_of_primes(int(sqrt(n)) + 1)
    factors = []
    for p in primes:
        while n % p == 0:
            factors.append(p)
            n = n // p
    if n > 1:
        factors.append(n)
    return factors


def prime_factorized(n):
    """Return all the prime factors of n
    360: [(2, 3), (3, 2), (5, 1)]"""
    pfs = prime_factors(n)
    return list((p, a) for p, a in Counter(pfs).items())


def phi(n):
    """Euler's totient function
    The number positive integers up to n
    that are relatively prime to n"""
    pfs = prime_factorized(n)
    r = 1
    for p, k in pfs:
        r *= (p - 1) * p ** (k - 1)
    return r


def factors(n):
    return set(
        reduce(
            list.__add__, ([i, n // i] for i in range(1, int(n**0.5) + 1) if n % i == 0)
        )
    )


def factors_from_prime_factors(pfs):
    prime_powers = [tuple(p**j for j in range(k + 1)) for p, k in pfs]
    return {prod(pp) for pp in product(*prime_powers)}


# f1 = factors(1440)
# f2 = factors_from_prime_factors(prime_factorized(1440))
# assert f1 == f2


def necklace_arrangements_2_colours(n):
    """Only rotational symmetry considered i.e. BBwwB = wwBBB
    Reflection symmetry is ignored i.e. counted twice
    for 2 arrangements reflectively the same"""
    fs = factors(n)
    r = 0
    for d in fs:
        r += phi(d) * (2 ** (n // d))
    return r // n


def bracelet_arrangements_2_colours(n):
    """Not just rotational symmetry considered
    Reflection symmetry also, so BBwwBBBw = wBBBwwBB
    """

    na = necklace_arrangements_2_colours(n)

    # an adjustment for the reflections
    if n % 2 == 1:
        a = 2 ** (n // 2)
    else:
        a = 2 ** (n // 2 - 1) + 2 ** (n // 2 - 2)

    return na // 2 + a


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
    n %= m
    _, t = extended_euclid(m, n)
    return t % m


def solve_congruences(congruences: list) -> int:
    """Given a list of congruence equations expressed as tuples.
    Check the moduli are all pairwise coprime

    X ≡ A1 (mod M1)
    ...
    X ≡ Ai (mod Mi)
    (A1,M1) , ... , (Ai,Mi)
    Return X ≡ LCM
    """
    # classes = [c[0] for c in congruences]
    moduli = [c[1] for c in congruences]
    chk = max(gcd(a, b) for a, b in combinations(moduli, 2))
    if chk != 1:
        raise ValueError("Moduli should be pairwise coprime")

    lcm_value = lcm(*moduli)
    total_cc = 0
    for a, m in congruences:
        other_moduli = [o for o in moduli if o != m]
        other_moduli_product = prod(other_moduli)
        inv = mod_inv(m, other_moduli_product)
        cc = a * other_moduli_product * inv
        total_cc += cc

    return total_cc % lcm_value


def mod_exp(b, e, m):
    """Return base^exp mod m using a binary method"""
    res = 1
    b %= m
    while e > 0:
        if e % 2 == 1:
            res = (res * b) % m
        e = e >> 1
        b = (b * b) % m
    return res


def extend_polynomial_sequence(seq, forward=1, backward=1, degree_limit=50):
    """Return the sequence extended forward and backwards a number of terms"""
    differences = [list(seq)]
    deg = 0
    while any(x != 0 for x in differences[-1]):
        deg += 1
        if deg > degree_limit:
            raise RuntimeError(f"Exceeded degree limit of {degree_limit}")
        difference = differences[-1]
        next_difference = [b - a for a, b in pairwise(difference)]
        differences.append(next_difference)

    new_differences = []
    for idx in range(len(differences) - 1, -1, -1):

        difference_to_extend = differences[idx]

        lower_difference = None
        if new_differences:
            lower_difference = new_differences[-1]

        for t in range(-forward, 0):
            d = 0
            if lower_difference:
                d = lower_difference[t]
            difference_to_extend += [difference_to_extend[-1] + d]

        for t in range(backward - 1, -1, -1):
            d = 0
            if lower_difference:
                d = lower_difference[t]
            difference_to_extend = [difference_to_extend[0] - d] + difference_to_extend

        new_differences.append(difference_to_extend)

    return new_differences[-1]


def search_for_polynomial_sequence(
    plots, l_bound, u_bound, deg=1, constants_required=3
) -> int:
    """Search for a polynomial sequence over evenly space terms
    Returns the spacing (modulus) and starting term"""
    m = l_bound
    while True:
        seq = plots[::m]
        for _ in range(deg):
            seq = [b - a for a, b in pairwise(seq)]
        if len(seq) > constants_required and len(set(seq[-constants_required:])) == 1:
            break

        if m > u_bound:
            raise RuntimeError("No sequence found")

        m += 1

    # so where does it start?
    # find the first inconsistent constant term
    for idx in range(len(seq) - 1, -1, -1):
        if seq[idx] != seq[-1]:
            break

    return m, idx + 1


def sum_arithmetic_seq(a, d, n):
    return (n * (2 * a + (n - 1) * d)) // 2


def sum_geometric_seq(a, r, n):
    return a * (r**n - 1) // (r - 1)


@lru_cache(maxsize=None)
def fibonacci(n):
    if n > 1:
        return fibonacci(n - 1) + fibonacci(n - 2)
    elif n == 1:
        return 1
    elif n == 0:
        return 0
    else:
        raise ValueError("negative n not allowed")


def zeckendorf(n):
    if n == 0:
        return [0]
    fib = [2, 1]
    while fib[0] < n:
        fib[0:0] = [sum(fib[:2])]
    dig = []
    for f in fib:
        if f <= n:
            dig, n = dig + [1], n - f
        else:
            dig += [0]
    return dig if dig[0] else dig[1:]


@lru_cache(maxsize=None)
def derangements(n):
    """Number of permutations of n such that no element remains in
    the same place

    recursively (n>2)
    !n = (n-1) x [ !(n-1) + !(n-2) ]

    or as a sum
    !n = n! x sum(i=0 to n) (-1)**i / i!
    (this shows as n 🡒 ∞, !n/n! 🡒 1/e by def of e)
    """
    if n > 1:
        return (n - 1) * (derangements(n - 1) + derangements(n - 2))
    elif n == 1:
        return 0
    elif n == 0:
        return 1
    else:
        raise ValueError("negative n not allowed")


# setrecursionlimit(2001)
# print(fibonacci(1000))
# print(derangements(1000))


@lru_cache(maxsize=None)
def bell_number(n):
    if 0 <= n <= 1:
        return 1
    return sum(comb(n - 1, k) * bell_number(k) for k in range(n))


def catalan_number(n):
    return comb(2 * n, n) // (n + 1)


# Pascal derivations


def bernoulli_triangle(n, k):
    return sum(comb(n, i) for i in range(k + 1))


def lazy_caterer(n):
    return bernoulli_triangle(n, 2)


def cake_number(n):
    return bernoulli_triangle(n, 3)


def circle_regions(n):
    return bernoulli_triangle(n, 4)
