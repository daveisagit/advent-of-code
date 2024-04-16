"""Advent of code 2015
--- Day 8: Matchsticks ---
"""

from collections import Counter
from common.aoc import file_to_list, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    data = raw_data
    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    cl = 0
    sl = 0
    for s in data:
        cl += len(s)
        s = eval(s)
        sl += len(s)
    return cl - sl


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    extra = 0
    for s in data:
        cnt = Counter(s)
        extra += cnt['"'] + cnt["\\"] + 2
    return extra


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)


MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)


solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
