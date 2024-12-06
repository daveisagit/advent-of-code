"""Advent of code 2024
--- Day 6: Guard Gallivant ---
"""

from operator import add

from common.aoc import (
    file_to_list,
    aoc_part,
    get_filename,
)


def parse_data(raw_data):
    """Parse the input"""
    grid = {}
    for ri, row in enumerate(raw_data):
        for ci, ch in enumerate(row):
            p = (ri, ci)
            if ch == "^":
                start = p
                grid[p] = "."
                continue
            grid[p] = ch

    return start, grid


directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def get_visited(start: tuple, grid: dict) -> set:
    """Return the visited positions, including the start"""
    d = 0
    p = start
    visited = {start}
    while True:
        dv = directions[d]
        np = tuple(map(add, p, dv))

        if np not in grid:
            break

        if grid[np] == "#":
            d += 1
            d %= 4
        else:
            p = np
            visited.add(p)

    return visited


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    start, grid = data
    visited = get_visited(start, grid)
    return len(visited)


def is_loop(start, grid) -> int:
    """Return True if we loop"""
    d = 0
    p = start
    pos = {(start, d)}
    while True:
        dv = directions[d]
        np = tuple(map(add, p, dv))

        if (np, d) in pos:
            return True

        if np not in grid:
            return False

        if grid[np] == "#":
            d += 1
            d %= 4
        else:
            p = np
            pos.add((p, d))


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    start, grid = data
    options = get_visited(start, grid)
    options.discard(start)

    cnt = 0
    for p in options:
        grid[p] = "#"
        if is_loop(start, grid):
            cnt += 1
        grid[p] = "."

    return cnt


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)


MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
