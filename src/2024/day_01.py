"""Advent of code 2024
--- Day 1: Historian Hysteria ---
"""

import re
from collections import Counter

from common.aoc import (
    file_to_list,
    aoc_part,
    get_filename,
)


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        sr = re.search(r"(-?\d+)\s+(-?\d+)", line)
        d = tuple(int(g) for g in sr.groups())
        data.append(d)
    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    l = sorted([a for a, b in data])
    r = sorted([b for a, b in data])
    d = list(zip(l, r))
    return sum(abs(a - b) for a, b in d)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    l = [a for a, b in data]
    r = [b for a, b in data]
    ctr = Counter(r)
    l = [x * ctr.get(x, 0) for x in l]
    return sum(l)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)


MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)


solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
