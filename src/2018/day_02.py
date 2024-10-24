"""Advent of code 2018
--- Day 2: Inventory Management System ---
"""

from collections import Counter
from itertools import combinations
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import string_differs_at


def parse_data(raw_data):
    """Parse the input"""
    data = raw_data
    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    c2 = 0
    c3 = 0
    for w in data:
        c = Counter(w)
        if 2 in c.values():
            c2 += 1
        if 3 in c.values():
            c3 += 1
    return c2 * c3


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    for p, a in enumerate(data[:-1]):
        for b in data[p + 1 :]:
            cnt = 0
            for i, c in enumerate(a):
                if c != b[i]:
                    cnt += 1
                    idx = i
            if cnt == 1:
                return a[:idx] + a[idx + 1 :]


@aoc_part
def solve_part_c(data) -> int:
    """Solve part B"""
    for a, b in combinations(data, 2):
        d = string_differs_at(a, b)
        if len(d) == 1:
            d = d[0]
            return a[:d] + a[d + 1 :]


MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(MY_DATA)
solve_part_b(MY_DATA)
solve_part_c(MY_DATA)
