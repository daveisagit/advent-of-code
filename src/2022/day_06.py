"""Advent of code 2022
--- Day 6: Tuning Trouble ---
"""

from common.aoc import file_to_string, aoc_part, get_filename
from common.general import window_over


def parse_data(raw_data):
    """Parse the input"""
    data = raw_data
    return data


def get_marker(data, msg_len=4):
    for idx, ss in enumerate(window_over(data, msg_len)):
        if len(set(list(ss))) == msg_len:
            break
    return idx + msg_len


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    return get_marker(data)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    return get_marker(data, msg_len=14)


EX_RAW_DATA = file_to_string(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
