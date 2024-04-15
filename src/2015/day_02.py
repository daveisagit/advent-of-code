"""Advent of code 2015
--- Day 2: I Was Told There Would Be No Math ---
"""

from itertools import combinations
from math import prod
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        t = tuple(int(x) for x in tok(line, "x"))
        data.append(t)
    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    total = 0
    for t in data:
        sides = [a * b for a, b in combinations(t, 2)]
        total += min(sides)
        total += 2 * sum(sides)
    return total


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    total = 0
    for t in data:
        sides = [2 * (a + b) for a, b in combinations(t, 2)]
        total += min(sides)
        total += prod(t)
    return total


MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(MY_DATA)

solve_part_b(MY_DATA)
