"""Advent of code 2020
--- Day 1: Report Repair ---
"""

from itertools import combinations
import math
from common.aoc import file_to_list, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    data = [int(v) for v in raw_data]
    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    for a, b in combinations(data, 2):
        if a + b == 2020:
            return a * b
    return None


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    for cmb in combinations(data, 3):
        if sum(cmb) == 2020:
            return math.prod(cmb)
    return None


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
