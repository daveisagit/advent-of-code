"""Advent of code 2015
--- Day 18: Like a GIF For Your Yard ---
"""

from operator import add
from common.aoc import file_to_list, aoc_part, get_filename
from common.grid_2d import get_grid_limits, grid_lists_to_dict, all_directions


def parse_data(raw_data):
    """Parse the input"""
    data = grid_lists_to_dict(raw_data)
    return data


def iterate(lights, corners=False):
    """Iterate"""
    min_r, min_c, max_r, max_c = get_grid_limits(lights)
    new_lights = {}
    for p, s in lights.items():
        if corners:
            r, c = p
            if (r in (min_r, max_r)) and (c in (min_c, max_c)):
                new_lights[p] = "#"
                continue
        nt = 0
        for d in all_directions:
            n = tuple(map(add, p, d))
            if n in lights and lights[n] == "#":
                nt += 1
        if s == "#":
            if 2 <= nt <= 3:
                new_lights[p] = "#"
            else:
                new_lights[p] = "."
        if s == ".":
            if nt == 3:
                new_lights[p] = "#"
            else:
                new_lights[p] = "."

    return new_lights


def draw(lights):
    """Visual"""
    min_r, min_c, max_r, max_c = get_grid_limits(lights)
    for r in range(min_r, max_r + 1):
        row = ""
        for c in range(min_c, max_c + 1):
            row += lights[(r, c)]
        print(row)


@aoc_part
def solve_part_a(lights, steps) -> int:
    """Solve part A"""
    for _ in range(steps):
        lights = iterate(lights)
    return sum(1 if x == "#" else 0 for x in lights.values())


@aoc_part
def solve_part_b(lights, steps) -> int:
    """Solve part B"""
    min_r, min_c, max_r, max_c = get_grid_limits(lights)
    lights[(min_r, min_c)] = "#"
    lights[(min_r, max_c)] = "#"
    lights[(max_r, min_c)] = "#"
    lights[(max_r, max_c)] = "#"
    for _ in range(steps):
        lights = iterate(lights, corners=True)
    return sum(1 if x == "#" else 0 for x in lights.values())


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA, 4)
solve_part_a(MY_DATA, 100)

solve_part_b(EX_DATA, 5)
solve_part_b(MY_DATA, 100)
