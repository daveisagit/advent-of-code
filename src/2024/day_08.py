"""Advent of code 2024
--- Day 8: Resonant Collinearity ---
"""

from collections import defaultdict
from itertools import combinations
from operator import add, sub

from common.aoc import (
    file_to_list,
    aoc_part,
    get_filename,
)


def get_antenna(data):
    """Return the locations of the antenna"""
    ALPHA_LOWER = "abcdefghijklmnopqrstuvwxyz"
    ALPHA_UPPER = ALPHA_LOWER.upper()
    DIGITS = "0123456789"
    labels = set(list(ALPHA_LOWER) + list(ALPHA_UPPER) + list(DIGITS))
    locs = defaultdict(set)
    sz = len(data)
    for ri, row in enumerate(data):
        for ci, ch in enumerate(row):
            p = (ri, ci)
            if ch in labels:
                locs[ch].add(p)
    return sz, locs


def parse_data(raw_data):
    sz, locs = get_antenna(raw_data)
    return sz, locs


def get_an(a, b):
    """For part A just 1 direction"""
    v = tuple(map(sub, a, b))
    c = tuple(map(add, b, v))
    c = tuple(map(add, c, v))
    return c


def get_ans(a, b, sz):
    """For part B every point on the line"""
    v = tuple(map(sub, a, b))
    ans = set()
    c = a
    while all(0 <= x < sz for x in c):
        ans.add(c)
        c = tuple(map(add, c, v))

    c = a
    while all(0 <= x < sz for x in c):
        ans.add(c)
        c = tuple(map(sub, c, v))

    return ans


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    sz, antenna = data
    an_locs = set()
    for locs in antenna.values():
        for a, b in combinations(locs, 2):
            an = get_an(a, b)
            if all(0 <= x < sz for x in an):
                an_locs.add(an)
            an = get_an(b, a)
            if all(0 <= x < sz for x in an):
                an_locs.add(an)

    return len(an_locs)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    sz, antenna = data
    an_locs = set()
    for locs in antenna.values():
        for a, b in combinations(locs, 2):
            ans = get_ans(a, b, sz)
            an_locs.update(ans)

    return len(an_locs)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
