"""Advent of code 2017
--- Day 1: Inverse Captcha ---
"""

from itertools import pairwise
from common.aoc import aoc_part, file_to_string, get_filename


def parse_data(raw_data):
    """Parse the input"""
    return [int(c) for c in raw_data]


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    s = 0
    for a, b in pairwise(data):
        if a == b:
            s += a
    if data[-1] == data[0]:
        s += data[-1]

    return s


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    l = len(data)
    l2 = l // 2
    s = 0
    for i, d in enumerate(data):
        i += l2
        i %= l
        if d == data[i]:
            s += d
    return s


EX_RAW_DATA = file_to_string(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
