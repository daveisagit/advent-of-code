"""Advent of code 2022
--- Day 4: Camp Cleanup ---
"""

import re
from common.aoc import file_to_list, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        rr = re.search(r"(\d+)-(\d+),(\d+)-(\d+)", line)
        range_data = [int(x) for x in rr.groups()]
        r1 = (range_data[0], range_data[1] + 1)
        r2 = (range_data[2], range_data[3] + 1)
        data.append((r1, r2))
    return data


def contains(a, b) -> bool:
    return a[0] >= b[0] and a[1] <= b[1]


def overlays(a, b) -> bool:
    return b[0] <= a[0] < b[1]


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    containers = [(r1, r2) for r1, r2 in data if contains(r1, r2) or contains(r2, r1)]
    return len(containers)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    overlayers = [(r1, r2) for r1, r2 in data if overlays(r1, r2) or overlays(r2, r1)]
    return len(overlayers)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
