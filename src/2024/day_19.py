"""Advent of code 2024
--- Day n: ---
"""

import json
import re

from collections import Counter, deque, defaultdict
from heapq import heappop, heappush
from itertools import pairwise, combinations, permutations, product
from math import inf, gcd, lcm, sqrt, comb, ceil, floor
from operator import add, sub

from common.aoc import (
    file_to_list,
    aoc_part,
    get_filename,
    file_to_string,
    file_to_list_no_strip,
)
from common.general import input_sections, tok, window_over
from common.grid_2d import directions, get_grid_limits, grid_lists_to_dict

show_parsed = False
show_parsed = True


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        sr = re.search(r"(-?\d+)\s+(-?\d+)", line)  # day 1

        sr = re.search(r"(.+) to (.+) = (\d+)", line)
        sr = re.search(r"(.{3}) = \((.{3}), (.{3})\)", line)
        sr = re.search(r"(\d+)-(\d+),(\d+)-(\d+)", line)
        u = sr.group(1)
        v = sr.group(2)
        d = int(sr.group(3))
        d = tuple(int(g) for g in sr.groups())

        data.append(d)

    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    return len(data)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    return len(data)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)
if show_parsed:
    print("Parsed data:")
    print(json.dumps(EX_DATA, indent=4))

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)
if show_parsed:
    print("Parsed data:")
    print(json.dumps(MY_DATA, indent=4))

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
