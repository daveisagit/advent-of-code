"""Advent of code 2017
--- Day 22: Sporifica Virus ---
"""

from operator import add
from common.aoc import file_to_list, aoc_part, get_filename
from common.grid_2d import get_grid_limits, grid_lists_to_dict, rotations


def parse_data(raw_data):
    """Parse the input"""
    centre = (len(raw_data) - 1) // 2
    centre = (centre, centre)
    data = grid_lists_to_dict(raw_data, content_filter="#")
    infections = set(data)
    return infections, centre


def burst(infections: set, pos, di, ic):
    """Do a burst, update infections
    return next position, direction index and counter for causing infection"""
    if pos in infections:
        di -= 1  # right
        infections.remove(pos)
    else:
        di += 1  # left
        infections.add(pos)
        ic += 1
    di %= 4
    d = rotations[di]
    pos = tuple(map(add, pos, d))
    return pos, di, ic


def draw(infections):
    """Visual"""
    min_r, min_c, max_r, max_c = get_grid_limits(infections)
    for r in range(min_r, max_r + 1):
        row = ""
        for c in range(min_c, max_c + 1):
            p = (r, c)
            ch = "."
            if p in infections:
                ch = "#"
            row += ch
        print(row)


state_char = [".", "W", "#", "F"]


def draw_b(states, cp):
    """Visual"""
    min_r, min_c, max_r, max_c = get_grid_limits(states)
    for r in range(min_r, max_r + 1):
        row = ""
        for c in range(min_c, max_c + 1):
            p = (r, c)
            ch = state_char[states.get(p, 0)]
            if p == cp:
                ch = "*"
            row += ch
        print(row)


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    infections, centre = data
    p = centre
    di = 1
    ic = 0
    for _ in range(10000):
        p, di, ic = burst(infections, p, di, ic)
    return ic


def burst_b(states, pos, di, ic):
    """Do a burst, update infections
    return next position, direction index and counter for causing infection"""
    st = states.get(pos, 0)
    if st == 0:
        di += 1  # left
    if st == 1:
        ic += 1  # no change, but inc counter
    if st == 2:
        di -= 1  # right
    if st == 3:
        di += 2  # reverse

    st += 1
    st %= 4
    states[pos] = st

    di %= 4
    d = rotations[di]
    pos = tuple(map(add, pos, d))
    return pos, di, ic


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    infections, centre = data
    p = centre
    di = 1
    ic = 0
    states = {p: 2 for p in infections}

    for _ in range(10000000):
        p, di, ic = burst_b(states, p, di, ic)

    return ic


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
