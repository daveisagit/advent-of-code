"""Advent of code 2016
--- Day 18: Like a Rogue ---
"""

from collections import Counter
from common.aoc import file_to_string, aoc_part, get_filename
from common.general import window_over


def parse_data(raw_data):
    """Parse the input"""
    data = raw_data
    return data


def next_row(s):
    """Return the next row"""
    prv = f".{s}."
    ns = ""
    for w in window_over(prv, 3):
        c = "."
        if w in ["^^.", ".^^", "^..", "..^"]:
            c = "^"
        ns += c
    return ns


@aoc_part
def solve_part_a(data, sz) -> int:
    """Solve part A"""
    s = data
    total = 0
    for _ in range(sz):
        cnt = Counter(s)
        total += cnt["."]
        s = next_row(s)

    return total


@aoc_part
def solve_part_b(data, sz) -> int:
    """Solve part B"""
    s = data
    total = 0
    for _ in range(sz):
        cnt = Counter(s)
        total += cnt["."]
        s = next_row(s)

    return total


EX_RAW_DATA = file_to_string(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA, 10)
solve_part_a(MY_DATA, 40)

solve_part_b(MY_DATA, 400000)
