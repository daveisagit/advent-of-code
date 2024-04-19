"""Advent of code 2015
--- Day 20: Infinite Elves and Infinite Houses ---
"""

from collections import Counter, defaultdict
from math import log2, prod, sqrt
from common.aoc import file_to_string, aoc_part, get_filename
from common.general import powerset
from common.numty import prime_factors, prime_list


def parse_data(raw_data):
    """Parse the input"""
    data = int(raw_data)
    return data


def unique_partitions_of(n):
    """Partitions"""
    answer = set()
    answer.add((n,))
    for x in range(1, n):
        for y in unique_partitions_of(n - x):
            answer.add(tuple(sorted((x,) + y, reverse=True)))
    return answer


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A
    The number of presents is 10x the sum of factors
    A factor sum is multiplicative fs(ab) = fs(a)fs(b) if a,b are coprime
    Also a fs(p^n) = 1 + p + p^2 + ... + p^n (sum of geometric series)

    So we only need to look at certain powers constrained by MP where 2^MP < Target
    We favour higher powers of the lower primes to keep N at a minimum
    """

    primes = list(prime_list(int(sqrt(data / 10)) + 1))
    max_no_of_prime_factors = int(log2(data / 10))
    ans = []

    for total_powers in range(1, max_no_of_prime_factors + 1):

        # get all unique partitions of total_powers
        # larger partitions to the left
        # we favour high powers of the lower primes
        possible_powers = sorted(
            unique_partitions_of(total_powers),
            key=lambda x: (-len(x), x),
            reverse=True,
        )

        for powers in possible_powers:
            n = 1
            fs = 1
            for i, p in enumerate(powers):
                n *= primes[i] ** p
                fs *= (primes[i] ** (p + 1) - 1) // (primes[i] - 1)
            if fs * 10 >= data:
                ans.append((n, fs))

    ans = sorted(ans, key=lambda x: x[0])
    return ans[0][0]


def analysis(data):
    house = defaultdict(int)
    c = 0
    elf = 0
    while True:
        # if house.values() and max(house.values()) >= data:
        #     break
        c += 1
        if c > 250000:
            break
        elf += 1
        for i in range(1, 51):
            h = elf * i
            house[h] += elf * 11

    house = [(h, p) for h, p in house.items()]
    house = sorted(house)
    for h, g in house[:500]:
        fs = 1
        pfs = prime_factors(h)
        pfz = list((p, a) for p, a in Counter(pfs).items())
        for p, a in pfz:
            fs *= (p ** (a + 1) - 1) // (p - 1)

        factors = {prod(x) for x in powerset(pfs)}
        factors = sorted(factors)
        factors = [f for f in factors if f * 50 < h]
        d = sum(factors)

        if g // 11 != fs - d:
            print(h, g, fs, g // 11, pfs, factors, fs - d)


def part_b_adjustment(n):
    """Return the amount lost due to elves dropping off after 50 deliveries
    This is the sum of factors where f x 50 < n"""
    pfs = prime_factors(n)
    factors = {prod(x) for x in powerset(pfs)}
    factors = sorted(factors)
    factors = [f for f in factors if f * 50 < n]
    return sum(factors)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B
    Same as part A but we need to adjust the factor sum
    """

    primes = list(prime_list(int(sqrt(data / 11)) + 1))
    max_no_of_prime_factors = int(log2(data / 11))
    ans = []

    for total_powers in range(1, max_no_of_prime_factors + 1):

        # get all unique partitions of total_powers
        # larger partitions to the left
        # we favour high powers of the lower primes
        possible_powers = sorted(
            unique_partitions_of(total_powers),
            key=lambda x: (-len(x), x),
            reverse=True,
        )

        for powers in possible_powers:
            n = 1
            fs = 1
            for i, p in enumerate(powers):
                n *= primes[i] ** p
                fs *= (primes[i] ** (p + 1) - 1) // (primes[i] - 1)

            # ignore very large values
            if fs > 10 * data:
                continue

            fs -= part_b_adjustment(n)
            if fs * 11 >= data:
                ans.append((n, fs))

    ans = sorted(ans, key=lambda x: x[0])
    return ans[0][0]


MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(MY_DATA)
# analysis(MY_DATA)
solve_part_b(MY_DATA)
