"""Advent of code 2024
--- Day 22: Monkey Market ---
"""

from collections import Counter
from itertools import pairwise

from common.aoc import file_to_list, aoc_part, get_filename
from common.general import window_over

M = 16777216


def parse_data(raw_data):
    """Parse the input"""
    data = [int(line) for line in raw_data]
    return data


def mix(n, sn):
    return n ^ sn


def prune(sn):
    return sn % M


def iterate(sn):
    """Return next secret number"""
    n = sn * 64
    sn = mix(n, sn)
    sn = prune(sn)

    n = sn // 32
    sn = mix(n, sn)
    sn = prune(sn)

    n = sn * 2048
    sn = mix(n, sn)
    sn = prune(sn)
    return sn


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    t = 0
    for n in data:
        for _ in range(2000):
            n = iterate(n)
        t += n

    return t


def get_seq(n) -> int:
    """Return the sequence of 1s digits for each iteration of a secret number"""
    sq = []
    # Each buyer is going to generate 2000 secret numbers after their initial secret number
    # so, for each buyer, you'll have 2000 price changes in which your sequence can occur.
    # !!! so we need this extra append !!!
    sq.append(n % 10)
    for _ in range(2000):
        n = iterate(n)
        sq.append(n % 10)
    return sq


def get_values_of_4_price(n):
    """Return a dict keyed on 4 prices with the value to use"""
    sq = get_seq(n)
    diff = [b - a for a, b in pairwise(sq)]
    price_values = {}
    for i, w in enumerate(window_over(diff, 4, 1)):
        w = tuple(w)
        if w not in price_values:
            v = sq[i + 4]
            price_values[w] = v
    return price_values


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    # get all sequences and all possible 4-price tuples
    # sort in order of popularity
    # find the best, quit if past whats possible

    price_values_for_every_n = []
    for n in data:
        price_values = get_values_of_4_price(n)
        price_values_for_every_n.append(price_values)

    print(f"Got all price values: {len(price_values_for_every_n)}")

    to_try = []
    for price_values in price_values_for_every_n:
        for pv_seq in price_values:
            to_try.append(pv_seq)
    to_try = Counter(to_try)
    to_try = sorted(to_try.items(), key=lambda x: x[1], reverse=True)
    print(f"All price values to try {len(to_try)}")

    best = 0
    best_pv = None
    for pv, cnt in to_try:

        # if the number of occurrences of this price value
        # is not large enough, then we are done
        if cnt * 9 < best:
            break

        # calc the total bananas
        bananas = 0
        for price_values in price_values_for_every_n:
            if pv not in price_values:
                continue
            bananas += price_values[pv]

        if bananas > best:
            best = bananas
            best_pv = pv

    print(f"Best price value: {best_pv}")
    return best


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)


MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)


solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
