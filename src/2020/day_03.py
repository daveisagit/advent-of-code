"""Advent of code 2020
--- Day 3: Toboggan Trajectory ---
"""

from common.aoc import file_to_list, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        trees = [i for i, c in enumerate(line) if c == "#"]
        data.append(trees)

    return data, len(raw_data[0])


def trees_hit(data, slope):
    """How many ?"""
    forest, col_width = data
    sr = slope[0]
    sc = slope[1]
    total = 0
    for r, trees in enumerate(forest[::sr]):
        c = (r * sc) % col_width
        if c in trees:
            total += 1
    return total


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    forest, col_width = data
    total = 0
    for r, trees in enumerate(forest):
        c = (r * 3) % col_width
        if c in trees:
            total += 1

    return total


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    slopes = ((1, 1), (1, 3), (1, 5), (1, 7), (2, 1))
    total = 1
    for slope in slopes:
        total *= trees_hit(data, slope)
    return total


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
