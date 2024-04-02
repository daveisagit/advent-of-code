"""Advent of code 2017
--- Day 19: A Series of Tubes ---
"""

from operator import add
from common.aoc import file_to_list_no_strip, aoc_part, get_filename
from common.grid_2d import grid_lists_to_dict, rotations


def parse_data(raw_data):
    """Parse the input"""
    start = raw_data[0].index("|")
    start = (0, start)
    data = grid_lists_to_dict(raw_data)
    return data, start


def trace_path(data, start, di=3):
    """Collected letters"""
    cp = start
    path = []
    steps = 0
    while True:
        steps += 1
        d = rotations[di]
        cp = tuple(map(add, cp, d))

        if cp not in data:
            break

        mc = data[cp]
        if mc == "+":

            di_l = (di + 1) % 4
            d_l = rotations[di_l]
            p = tuple(map(add, cp, d_l))
            if data.get(p, " ") != " ":
                di = di_l
                continue

            di_r = (di - 1) % 4
            d_r = rotations[di_r]
            p = tuple(map(add, cp, d_r))
            if data.get(p, " ") != " ":
                di = di_r
                continue

        if mc.isalpha():
            path.append(mc)
            continue

        if mc in ("|-"):
            continue

        break

    return path, steps


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    grid, start = data
    p, _ = trace_path(grid, start)
    return "".join(p)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    grid, start = data
    _, steps = trace_path(grid, start)
    return steps


EX_RAW_DATA = file_to_list_no_strip(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list_no_strip(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
