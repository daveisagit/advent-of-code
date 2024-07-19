"""Advent of code 2022
--- Day 12: Hill Climbing Algorithm ---
"""

from collections import defaultdict
from operator import add
from common.aoc import file_to_list, aoc_part, get_filename
from common.graph import dijkstra
from common.grid_2d import directions


def parse_data(raw_data):
    """Parse the input"""
    new_grid = {}
    for ri, row in enumerate(raw_data):
        for ci, height in enumerate(row):
            p = (ri, ci)
            if height == "S":
                start = p
                height = "a"
            if height == "E":
                end = p
                height = "z"
            new_grid[p] = height
    return new_grid, start, end


def make_graph_a(grid):
    """Valid routes from S->E"""
    gph = defaultdict(dict)
    for p, h in grid.items():
        for d in directions.values():
            n = tuple(map(add, p, d))
            if n in grid and ord(grid[n]) <= ord(h) + 1:
                gph[p][n] = 1
    return gph


def make_graph_b(grid):
    """Valid routes from E->S"""
    gph = defaultdict(dict)
    for p, h in grid.items():
        for d in directions.values():
            n = tuple(map(add, p, d))
            if n in grid and ord(h) - 1 <= ord(grid[n]):
                gph[p][n] = 1
    return gph


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    grid, start, end = data
    gph = make_graph_a(grid)
    return dijkstra(gph, start, end)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    grid, _, end = data
    gph = make_graph_b(grid)
    distances_from_end = dijkstra(gph, end, None)
    return min(d for p, d in distances_from_end.items() if grid[p] == "a")


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
