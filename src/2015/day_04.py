"""Advent of code 2015
--- Day 4: The Ideal Stocking Stuffer ---
"""

from hashlib import md5
from common.aoc import file_to_string, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    data = raw_data
    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    i = 0
    while True:
        i += 1
        s = f"{data}{i}".encode()
        h = md5(s).hexdigest()
        if h[:5] == "00000":
            return i


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    i = 0
    while True:
        i += 1
        s = f"{data}{i}".encode()
        h = md5(s).hexdigest()
        if h[:6] == "000000":
            return i


EX_RAW_DATA = file_to_string(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(MY_DATA)
