"""Advent of code 2015
--- Day 12: JSAbacusFramework.io ---
"""

import json
from common.aoc import file_to_string, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    data = json.loads(raw_data)
    return data


def number_sum(data, ignore_red=False):
    """Total the integers"""
    if not isinstance(data, (list, dict)):
        if isinstance(data, int):
            return data
        return 0

    if isinstance(data, dict):
        if ignore_red and "red" in data.values():
            return 0
        return number_sum(list(data.values()), ignore_red=ignore_red)

    if isinstance(data, list):
        return sum(number_sum(i, ignore_red=ignore_red) for i in data)


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    return number_sum(data)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    return number_sum(data, ignore_red=True)


MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(MY_DATA)

solve_part_b(MY_DATA)
