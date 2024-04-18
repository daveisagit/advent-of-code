"""Advent of code 2015
--- Day 17: No Such Thing as Too Much ---
"""

from itertools import combinations
from common.aoc import file_to_list, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    data = [int(x) for x in raw_data]
    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    cnt = 0
    for noc in range(1, len(data) + 1):
        for c in combinations(data, noc):
            if sum(c) == 150:
                cnt += 1

    return cnt


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    cnt = 0
    for noc in range(1, len(data) + 1):
        for c in combinations(data, noc):
            if sum(c) == 150:
                cnt += 1
        if cnt > 0:
            break

    return cnt


MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(MY_DATA)

solve_part_b(MY_DATA)
