"""Advent of code 2022
--- Day 14: Regolith Reservoir ---
"""

from itertools import pairwise
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    veins = []
    for line in raw_data:
        points = tok(line, "->")
        vein = []
        for point in points:
            point = tuple(int(x) for x in tok(point, ","))
            vein.append(point)
        veins.append(vein)
    return veins


def create_state(veins):
    """Return a dict of point: content where content = # for wall"""
    state = {}
    for vein in veins:
        for a, b in pairwise(vein):
            min_x = min(a[0], b[0])
            max_x = max(a[0], b[0])
            min_y = min(a[1], b[1])
            max_y = max(a[1], b[1])
            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
                    state[(x, y)] = "#"
    return state


def find_rest_point(state, here, depth, floor=None):
    """Recursively look for where the sand stops"""
    x, y = here

    if floor and y + 1 == floor:
        return here

    if y > depth + 3:
        return None
    if (x, y + 1) not in state:
        return find_rest_point(state, (x, y + 1), depth, floor=floor)
    if (x - 1, y + 1) not in state:
        return find_rest_point(state, (x - 1, y + 1), depth, floor=floor)
    if (x + 1, y + 1) not in state:
        return find_rest_point(state, (x + 1, y + 1), depth, floor=floor)
    return here


def get_depth(state):
    return max(rock[1] for rock in state.keys())


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    state = create_state(data)
    depth = get_depth(state)
    walls = len(state)

    p = find_rest_point(state, (500, 0), depth)
    while p:
        state[p] = "+"
        p = find_rest_point(state, (500, 0), depth)

    return len(state) - walls


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    state = create_state(data)
    depth = get_depth(state)
    walls = len(state)

    p = find_rest_point(state, (500, 0), depth, floor=depth + 2)
    while p:
        state[p] = "+"
        if p == (500, 0):
            break
        p = find_rest_point(state, (500, 0), depth, floor=depth + 2)

    return len(state) - walls


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
