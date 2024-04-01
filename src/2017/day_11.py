"""Advent of code 2017
--- Day 11: Hex Ed ---
"""

from operator import add
from common.aoc import aoc_part, file_to_string, get_filename
from common.general import tok


hex_map = {
    "s": (0, -2),
    "ne": (1, 1),
    "nw": (-1, 1),
    "n": (0, 2),
    "sw": (-1, -1),
    "se": (1, -1),
}


def parse_data(raw_data):
    """Parse the input"""
    return tok(raw_data, ",")


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    p = (0, 0)
    for d in data:
        d = hex_map[d]
        p = tuple(map(add, p, d))

    x = abs(p[0])
    y = abs(p[1])
    c = max(y - x, 0)

    return x + c // 2


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    p = (0, 0)
    farthest = 0
    for d in data:
        d = hex_map[d]
        p = tuple(map(add, p, d))

        x = abs(p[0])
        y = abs(p[1])
        c = max(y - x, 0)
        md = x + c // 2
        farthest = max(farthest, md)

    return farthest


EX_RAW_DATA = file_to_string(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
