"""Advent of code 2024
--- Day 2: Red-Nosed Reports ---
"""

from itertools import pairwise

from common.aoc import (
    file_to_list,
    aoc_part,
    get_filename,
)
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        arr = tok(line)
        d = tuple(int(x) for x in arr)
        data.append(d)
    return data


def safe_1(d):
    df = sorted(d)
    dr = sorted(d, reverse=True)
    dl = list(d)
    return dl == df or dl == dr


def safe_2(d):
    for a, b in pairwise(d):
        if not (1 <= abs(a - b) <= 3):
            return False
    return True


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    cnt = 0
    for d in data:
        if safe_1(d) and safe_2(d):
            cnt += 1
    return cnt


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    cnt = 0
    for d in data:
        safe = False
        for i in range(len(d)):
            c = list(d)
            c.pop(i)
            if safe_1(c) and safe_2(c):
                safe = True
                break
        if safe:
            cnt += 1

    return cnt


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
