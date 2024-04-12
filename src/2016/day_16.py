"""Advent of code 2016
--- Day 16: Dragon Checksum ---
"""

from common.aoc import file_to_string, aoc_part, get_filename
from common.general import window_over


def parse_data(raw_data):
    """Parse the input"""
    data = raw_data
    return data


def iterate(s):
    """Next Dragon string"""
    s2 = list(s)
    s2 = list(reversed(s2))
    s2 = ["1" if b == "0" else "0" for b in s2]
    s2 = "".join(s2)
    return f"{s}0{s2}"


def get_checksum(s):
    """Checksum"""
    while len(s) % 2 == 0:
        ns = ""
        for d in window_over(s, 2, 2):
            b = "0"
            if d[0] == d[1]:
                b = "1"
            ns += b
        s = ns
    return s


@aoc_part
def solve_part_a(data, sz) -> int:
    """Solve part A"""
    s = data
    while len(s) < sz:
        s = iterate(s)
    s = s[:sz]
    return get_checksum(s)


@aoc_part
def solve_part_b(data, sz) -> int:
    """Solve part B"""
    s = data
    while len(s) < sz:
        s = iterate(s)
    s = s[:sz]
    return get_checksum(s)


EX_RAW_DATA = file_to_string(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA, 20)
solve_part_a(MY_DATA, 272)

solve_part_b(MY_DATA, 35651584)
