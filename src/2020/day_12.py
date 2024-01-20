"""Advent of code 2020
--- Day 12: Rain Risk ---
"""

from operator import add
from common.aoc import file_to_list, aoc_part, get_filename
from common.grid_2d import rotate90, rotations, compass


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        data.append((line[0], int(line[1:])))
    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    pos = (0, 0)
    facing = 0
    for action, qty in data:
        if action == "L":
            facing += qty // 90
            facing %= 4
            continue

        if action == "R":
            facing -= qty // 90
            facing %= 4
            continue

        if action == "F":
            d = rotations[facing]

        if action in "NEWS":
            d = compass[action]

        d = (v * qty for v in d)
        pos = tuple(map(add, pos, d))

    return abs(pos[0]) + abs(pos[1])


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    pos = (0, 0)
    wp = (-1, 10)
    for action, qty in data:
        if action == "L":
            for _ in range(qty // 90):
                wp = rotate90(wp)
            continue

        if action == "R":
            for _ in range(4 - (qty // 90)):
                wp = rotate90(wp)
            continue

        if action == "F":
            to_wp = tuple(v * qty for v in wp)
            pos = tuple(map(add, pos, to_wp))

        if action in "NEWS":
            d = compass[action]
            d = (v * qty for v in d)
            wp = tuple(map(add, wp, d))

    return abs(pos[0]) + abs(pos[1])


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)


MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)


solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
