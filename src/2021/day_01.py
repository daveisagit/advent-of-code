"""Advent of code 2021
--- Day 1: Sonar Sweep ---
"""


from itertools import pairwise
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import window_over


def parse_data(raw_data):
    """Parse the input"""
    data = [int(x) for x in raw_data]
    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    pairs = pairwise(data)
    increases = [1 if b > a else 0 for a, b in pairs]
    return sum(increases)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    window_sums = [sum(window) for window in window_over(data, 3)]
    pairs = pairwise(window_sums)
    increases = [1 if b > a else 0 for a, b in pairs]
    return sum(increases)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
