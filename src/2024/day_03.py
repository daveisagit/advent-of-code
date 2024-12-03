"""Advent of code 2024
--- Day 3: Mull It Over ---
"""

import re
from math import prod
from common.aoc import (
    aoc_part,
    get_filename,
    file_to_string,
)


def parse_data(raw_data):
    """Parse the input"""
    return raw_data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    sr = re.findall(r"mul\((\d+),(\d+)\)", data)
    mlt = [int(a) * int(b) for a, b in sr]
    return sum(mlt)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    rx = re.compile(r"mul\(\d+,\d+\)|do\(\)|don't\(\)")
    sr = rx.finditer(data)
    # dont need start() as the iter will be sorted as found
    # but here for reference
    res = [(occ.start(), occ.group()) for occ in sr]
    enabled = True
    s = 0
    for _, v in res:
        if v == "do()":
            enabled = True
            continue
        if v == "don't()":
            enabled = False
            continue
        if enabled:
            sr = re.search(r"mul\((\d+),(\d+)\)", v)
            r = tuple(int(g) for g in sr.groups())
            s += prod(r)

    return s


EX_RAW_DATA = file_to_string(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
