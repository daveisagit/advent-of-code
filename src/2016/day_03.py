"""Advent of code 2016
--- Day 3: Squares With Three Sides ---
"""

import re
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import window_over


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        rr = re.search(r"(\d+)\s+(\d+)\s+(\d+)", line)
        t = [int(x) for x in rr.groups()]
        data.append(t)
    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    triangles = [sorted(t) for t in data]
    return sum(1 for tri in triangles if (tri[0] + tri[1]) > tri[2])


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    total = 0
    for c in range(3):
        col = [t[c] for t in data]
        triangles = [sorted(t) for t in window_over(col, 3, 3)]
        legit = sum(1 for tri in triangles if (tri[0] + tri[1]) > tri[2])
        total += legit

    return total


MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(MY_DATA)
solve_part_b(MY_DATA)
