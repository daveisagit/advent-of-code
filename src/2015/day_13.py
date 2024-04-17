"""Advent of code 2015
--- Day 13: Knights of the Dinner Table ---
"""

from collections import defaultdict
from itertools import pairwise, permutations
import re
from common.aoc import file_to_list, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    gph = defaultdict(dict)
    for line in raw_data:
        rr = re.search(
            r"(.+) would (gain|lose) (\d+) happiness units by sitting next to (.+).",
            line,
        )
        v = int(rr.group(3))
        if rr.group(2) == "lose":
            v = -v
        gph[rr.group(1)][rr.group(4)] = v

    return gph


@aoc_part
def solve_part_a(gph) -> int:
    """Solve part A"""
    happiest = 0
    for p in permutations(gph):
        p = list(p)
        p.append(p[0])
        happiness = 0
        for a, b in pairwise(p):
            happiness += gph[a][b]
            happiness += gph[b][a]
        happiest = max(happiest, happiness)

    return happiest


@aoc_part
def solve_part_b(gph) -> int:
    """Solve part B"""
    guests = list(gph.keys())
    for g in guests:
        gph["Me"][g] = 0
        gph[g]["Me"] = 0

    happiest = 0
    for p in permutations(gph):
        p = list(p)
        p.append(p[0])
        happiness = 0
        for a, b in pairwise(p):
            happiness += gph[a][b]
            happiness += gph[b][a]
        happiest = max(happiest, happiness)

    return happiest


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(MY_DATA)
