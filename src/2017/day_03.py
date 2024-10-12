"""Advent of code 2017
--- Day 3: Spiral Memory ---
"""

from math import ceil, floor, sqrt
from operator import add
from common.aoc import aoc_part, file_to_string, get_filename
from common.grid_2d import manhattan, spiral_location


def parse_data(raw_data):
    """Parse the input"""
    data = int(raw_data)
    return data


def get_md(n):
    """Return co-ord of n"""
    r = floor(ceil(sqrt(n)) / 2)
    axes_base = (2 * r - 1) ** 2 + r
    axes = [2 * r * x + axes_base for x in range(4)]
    d = min(abs(n - a) for a in axes)
    return d + r


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    r = get_md(data)
    # test spiral_location function
    loc = spiral_location(data, base=1)
    assert manhattan(loc) == r
    return r


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    directions = (
        (-1, 0),
        (0, -1),
        (1, 0),
        (0, 1),
    )
    diagonals = (
        (1, 1),
        (1, -1),
        (-1, 1),
        (-1, -1),
    )

    def val():
        nonlocal grid
        s = 0
        for d in directions:
            p = tuple(map(add, pos, d))
            s += grid.get(p, 0)
        for d in diagonals:
            p = tuple(map(add, pos, d))
            s += grid.get(p, 0)
        return s

    grid = {}
    pos = (0, 0)
    grid[pos] = 1
    dist = 0
    while True:
        pos = tuple(map(add, pos, (1, 1)))
        dist += 2
        for d in directions:
            for _ in range(dist):
                pos = tuple(map(add, pos, d))
                v = val()
                grid[pos] = v
                if v > data:
                    return v


EX_RAW_DATA = file_to_string(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)


MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)


solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(MY_DATA)
