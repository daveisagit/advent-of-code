"""Advent of code 2023
--- Day n: ---
"""

import json
from common.aoc import file_to_list, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    data = raw_data
    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    return len(data)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    return len(data)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)
# print("Parsed data:")
# print(json.dumps(EX_DATA, indent=4))

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)
# print("Parsed data:")
# print(json.dumps(MY_DATA, indent=4))

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
