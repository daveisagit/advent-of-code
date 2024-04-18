"""Advent of code 2015
--- Day 16: Aunt Sue ---
"""

import re
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import window_over

TT = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}

GT = ["cats", "trees"]
LT = ["pomeranians", "goldfish"]


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        rr = re.search(r"Sue \d+: (.+): (\d+), (.+): (\d+), (.+): (\d+)", line)
        sue = {g: int(v) for g, v in window_over(rr.groups(), 2, 2)}
        data.append(sue)
    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    for i, sue in enumerate(data):
        if all(v == TT[k] for k, v in sue.items()):
            return i + 1
    return None


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""

    def matches(k, v):
        if k in GT and v > TT[k]:
            return True
        if k in LT and v < TT[k]:
            return True
        if k not in GT and k not in LT:
            return v == TT[k]
        return False

    for i, sue in enumerate(data):
        if all(matches(k, v) for k, v in sue.items()):
            return i + 1
    return None


MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(MY_DATA)

solve_part_b(MY_DATA)
