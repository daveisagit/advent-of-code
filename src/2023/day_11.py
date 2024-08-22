"""Advent of code 2023
--- Day 11: Cosmic Expansion ---
"""

from bisect import bisect_left
from itertools import combinations
from common.aoc import file_to_list, aoc_part, get_filename
from common.grid_2d import grid_lists_to_dict, get_grid_limits, manhattan


def parse_data(raw_data):
    """Parse the input"""
    data = grid_lists_to_dict(raw_data, content_filter="#")
    return set(data)


def expand(data, addition=1):
    """Find the empty rows and columns and return the expanded result"""
    min_r, min_c, max_r, max_c = get_grid_limits(data)
    empty_rows = []
    empty_cols = []
    for r in range(min_r, max_r + 1):
        contents = [x for x in data if x[0] == r]
        if not contents:
            empty_rows.append(r)
    for c in range(min_c, max_c + 1):
        contents = [x for x in data if x[1] == c]
        if not contents:
            empty_cols.append(c)

    new_data = set()
    for p in data:
        i = bisect_left(empty_rows, p[0])
        r = p[0] + i * addition
        i = bisect_left(empty_cols, p[1])
        c = p[1] + i * addition
        new_data.add((r, c))
    return new_data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    data = expand(data)
    return sum(manhattan(a, b) for a, b in combinations(data, 2))


@aoc_part
def solve_part_b(data, factor=2) -> int:
    """Solve part B"""
    addition = factor - 1
    data = expand(data, addition=addition)
    return sum(manhattan(a, b) for a, b in combinations(data, 2))


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA, factor=100)
solve_part_b(MY_DATA, factor=100000)
