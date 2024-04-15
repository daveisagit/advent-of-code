"""Advent of code 2015
--- Day 3: Perfectly Spherical Houses in a Vacuum ---
"""

from collections import defaultdict
from operator import add
from common.aoc import file_to_string, aoc_part, get_filename
from common.grid_2d import directions


def parse_data(raw_data):
    """Parse the input"""
    return raw_data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    cp = (0, 0)
    locs = defaultdict(int)
    locs[cp] = 1
    for ch in data:
        d = directions[ch]
        cp = tuple(map(add, cp, d))
        locs[cp] += 1
    return len(locs)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    p = [(0, 0), (0, 0)]
    locs = defaultdict(int)
    locs[(0, 0)] = 2
    i = 0
    for ch in data:
        d = directions[ch]
        p[i] = tuple(map(add, p[i], d))
        locs[p[i]] += 1
        i = 1 - i
    return len(locs)


EX_RAW_DATA = file_to_string(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)
# print("Parsed data:")
# print(json.dumps(EX_DATA, indent=4))

MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)
# print("Parsed data:")
# print(json.dumps(MY_DATA, indent=4))

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
