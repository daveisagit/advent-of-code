"""Advent of code 2016
--- Day 15: Timing is Everything ---
"""

import re
from common.aoc import file_to_list, aoc_part, get_filename
from common.numty import solve_congruences


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        rr = re.search(
            r"Disc #\d has (\d+) positions; at time=(\d+), it is at position (\d+).",
            line,
        )
        t = tuple(int(x) for x in rr.groups())
        data.append(t)
    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    # Solve congruences
    # T0 + Disc# + pos = 0 (mod m
    # So T0 = -(disk+pos) (mod m)
    cg = [(-(t[2] + i + 1) % t[0], t[0]) for i, t in enumerate(data)]
    return solve_congruences(cg)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    data = data.copy()
    data.append((11, 0, 0))
    cg = [(-(t[2] + i + 1) % t[0], t[0]) for i, t in enumerate(data)]
    return solve_congruences(cg)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(MY_DATA)
