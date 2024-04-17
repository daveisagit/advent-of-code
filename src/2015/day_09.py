"""Advent of code 2015
--- Day 9: All in a Single Night ---
Careful, it's shorter to visit in between nodes! (Very odd)
"""

from collections import defaultdict
from itertools import pairwise, permutations
from math import inf
import re
from common.aoc import file_to_list, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    gph = defaultdict(dict)
    for line in raw_data:
        rr = re.search(r"(.+) to (.+) = (\d+)", line)
        u = rr.group(1)
        v = rr.group(2)
        d = int(rr.group(3))
        gph[u][v] = d
        gph[v][u] = d

    return gph


@aoc_part
def solve_part_a(gph) -> int:
    """Solve part A"""
    shortest = inf
    for p in permutations(set(gph)):
        total = 0
        for u, v in pairwise(p):
            total += gph[u][v]
        shortest = min(total, shortest)
    return shortest


@aoc_part
def solve_part_b(gph) -> int:
    """Solve part B"""
    longest = 0
    for p in permutations(set(gph)):
        total = 0
        for u, v in pairwise(p):
            total += gph[u][v]
        longest = max(total, longest)
    return longest


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(MY_DATA)
