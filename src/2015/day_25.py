"""Advent of code 2015
--- Day 25: Let It Snow ---
"""

import re
from common.aoc import file_to_string, aoc_part, get_filename
from common.numty import mod_exp


def parse_data(raw_data):
    """Parse the input"""
    rr = re.search(r".+ row (\d+), column (\d+).", raw_data)
    return tuple(int(x) for x in rr.groups())


def T(n):
    """Triangle no."""
    return n * (n + 1) // 2


def nth_term(r, c):
    """Diagonal nth term"""
    a = T(r - 1) + 1
    d = T(r + c - 1) - T(r)
    return a + d


def value_at(r, c):
    """Get nth term and use mod exponent"""
    tn = nth_term(r, c)
    mlt = mod_exp(252533, tn - 1, 33554393)
    ans = 20151125 * mlt
    ans %= 33554393
    return ans


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    r, c = data
    return value_at(r, c)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    return len(data)


MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(MY_DATA)
