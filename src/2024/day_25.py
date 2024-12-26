"""Advent of code 2024
--- Day 25: Code Chronicle ---
"""

from collections import Counter
from itertools import product

from common.aoc import file_to_list, aoc_part, get_filename
from common.general import input_sections
from common.grid_2d import (
    dict_get_col_as_list,
    dict_get_row_as_list,
    grid_lists_to_dict,
)


def parse_data(raw_data):
    """Parse the input"""
    keys = []
    locks = []
    for sec in input_sections(raw_data):
        g = grid_lists_to_dict(sec)
        r0 = dict_get_row_as_list(g, 0)
        lock = all(x == "#" for x in r0)
        profile = []
        for c in range(5):
            l = dict_get_col_as_list(g, c)
            cnt = Counter(l)
            profile.append(cnt["#"] - 1)
        profile = tuple(profile)
        if lock:
            locks.append(profile)
        else:
            keys.append(profile)

    return locks, keys


def matches(lock, key):
    for l, k in zip(lock, key):
        if l + k > 5:
            return False
    return True


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    locks, keys = data
    cnt = 0
    for l, k in product(locks, keys):
        if matches(l, k):
            cnt += 1

    return cnt


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)


solve_part_a(EX_DATA)
solve_part_a(MY_DATA)
