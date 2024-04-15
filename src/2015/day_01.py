"""Advent of code 2015
--- Day 1: Not Quite Lisp ---
"""

from collections import Counter
import json
from common.aoc import file_to_string, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    data = raw_data
    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    cnt = Counter(data)
    return cnt["("] - cnt[")"]


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    lvl = 0
    for i, ch in enumerate(data):
        if ch == "(":
            lvl += 1
        else:
            lvl -= 1
        if lvl < 0:
            break

    return i + 1


MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)


solve_part_a(MY_DATA)

solve_part_b(MY_DATA)
