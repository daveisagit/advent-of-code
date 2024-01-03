"""Advent of code 2021
--- Day 2: Dive! ---
"""


import math
from operator import add
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok

directions = {
    "forward": (0, 1),
    "down": (1, 0),
    "up": (-1, 0),
}


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        arr = tok(line)
        data.append((arr[0], int(arr[1])))
    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    cur_pos = (0, 0)
    for d, m in data:
        v = directions.get(d)
        move = tuple(o * m for o in v)
        cur_pos = tuple(map(add, cur_pos, move))
    return math.prod(cur_pos)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    aim = 0
    h_pos = 0
    depth = 0
    for d, m in data:
        if d == "down":
            aim += m
        if d == "up":
            aim -= m
        if d == "forward":
            h_pos += m
            depth += m * aim

    return h_pos * depth


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
