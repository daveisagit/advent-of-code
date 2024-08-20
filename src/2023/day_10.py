"""Advent of code 2023
--- Day 10: Pipe Maze ---
"""

from collections import defaultdict
from itertools import pairwise
from operator import add
from common.aoc import file_to_list, aoc_part, get_filename
from common.grid_2d import grid_lists_to_dict, directions_UDLR

symbols = {
    "L": "UR",
    "J": "UL",
    "7": "DL",
    "F": "DR",
    "|": "UD",
    "-": "LR",
    "S": "",
}


def parse_data(raw_data):
    """Parse the input"""
    cells = grid_lists_to_dict(raw_data, content_filter=symbols)
    start = None
    gph = defaultdict(dict)
    for p, ch in cells.items():
        if ch == "S":
            start = p
            continue
        for d in symbols[ch]:
            dv = directions_UDLR[d]
            n = tuple(map(add, p, dv))
            gph[p][n] = 1

    for dv in directions_UDLR.values():
        n = tuple(map(add, start, dv))
        if start in gph[n]:
            gph[start][n] = 1

    return gph, start


def find_loop(gph, start):
    """Given the graph and the start point find the loop"""
    loop = [start]
    visited = {start}
    while True:
        # where next for the end of the loop ?
        # ignore where we have been except for the start
        # if the loop is long enough start means we're done
        for n in gph[loop[-1]]:
            if n == start and len(loop) > 1:
                return loop
            if n in visited:
                continue
            loop.append(n)
            visited.add(n)
            break


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    gph, start = data
    loop = find_loop(gph, start)
    return len(loop) // 2


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""

    # Picks theorem
    # A = i + b/2 - 1
    # i = A + 1 - b/2
    gph, start = data
    loop = find_loop(gph, start)
    loop.append(start)

    # Area is calculated by summing slice heights going left
    # and subtracting them going right
    area = 0
    for a, b in pairwise(loop):
        w = a[1] - b[1]
        h = a[0]
        area += w * h
    area = abs(area)
    return area + 1 - len(loop) // 2


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

EX_RAW_DATA = file_to_list(get_filename(__file__, "xb"))
EX_DATA = parse_data(EX_RAW_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
