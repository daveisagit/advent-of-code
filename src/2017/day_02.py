"""Advent of code 2017
--- Day 2: Corruption Checksum ---
"""

from itertools import combinations
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        row = [int(x) for x in tok(line)]
        data.append(row)
    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    ans = sum(max(row) - min(row) for row in data)
    return ans


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    s = 0
    for row in data:
        for a, b in combinations(row, 2):
            if a > b:
                a, b = b, a
            if b % a == 0:
                s += b // a
                break
    return s


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
