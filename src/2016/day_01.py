"""Advent of code 2016
--- Day 1: No Time for a Taxicab ---
"""

from operator import add
from common.aoc import file_to_string, aoc_part, get_filename
from common.general import tok
from common.grid_2d import rotations, manhattan


def parse_data(raw_data):
    """Parse the input"""
    steps = tok(raw_data, ",")
    steps = [(s[0], int(s[1:])) for s in steps]
    return steps


@aoc_part
def solve_part_a(steps) -> int:
    """Solve part A"""
    cp = (0, 0)
    di = 1

    for t, w in steps:
        if t == "R":
            di -= 1
        else:
            di += 1
        di = di % 4
        d = rotations[di]
        d = tuple(x * w for x in d)
        cp = tuple(map(add, cp, d))

    return manhattan(cp)


@aoc_part
def solve_part_b(steps) -> int:
    """Solve part B"""
    cp = (0, 0)
    di = 1
    seen = set()
    for t, w in steps:
        if t == "R":
            di -= 1
        else:
            di += 1
        di = di % 4
        d = rotations[di]

        for _ in range(w):
            cp = tuple(map(add, cp, d))
            if cp in seen:
                return manhattan(cp)
            seen.add(cp)


EX_RAW_DATA = file_to_string(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)


MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
