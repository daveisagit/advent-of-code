"""Advent of code 2024
--- Day 12: Garden Groups ---
"""

from collections import deque
from operator import add

from common.aoc import (
    file_to_list,
    aoc_part,
    get_filename,
)
from common.graph import tarjan
from common.grid_2d import directions


def parse_data(raw_data):
    """Parse the input"""
    grid = {}
    sz = len(raw_data)
    for ri, row in enumerate(raw_data):
        for ci, ch in enumerate(row):
            p = (ri, ci)
            grid[p] = ch
    return sz, grid


def flood_fill(grid, p) -> set:
    """Return a set of points matching the value of p in the grid"""
    ch = grid[p]
    bfs = deque()
    seen = set()
    bfs.append(p)
    while bfs:
        p = bfs.popleft()
        if p in seen:
            continue
        seen.add(p)

        for dv in directions.values():
            np = tuple(map(add, p, dv))
            if np not in grid:
                continue
            if grid[np] != ch:
                continue
            bfs.append(np)

    return seen


def get_plots(sz, grid) -> list:
    """Return a list of plots, each plot is a set of points"""
    points_assessed = set()
    plots = []
    for r in range(sz):
        for c in range(sz):
            p = (r, c)
            if p in points_assessed:
                continue
            plot = flood_fill(grid, p)
            plots.append(plot)
            points_assessed |= plot
    return plots


def get_perimeter_points(plot) -> set:
    """Return a set of (p,d) representing a unit of perimeter
    p is the point outside the plot (either | or -)
    d is a direction
    """
    # any edge from p to a neighbour not in the plot
    # must be a unit of perimeter
    pd_set = set()
    for p in plot:
        for d, dv in directions.items():
            np = tuple(map(add, p, dv))
            if np not in plot:
                pd_set.add((np, d))
    return pd_set


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    sz, grid = data
    plots = get_plots(sz, grid)
    ans = 0
    for plot in plots:
        ans += len(plot) * len(get_perimeter_points(plot))
    return ans


def get_sides(plot) -> int:
    """Return the number of sides the plot has"""

    # 2 units of perimeter are on the same side next to each other
    # if their
    #   direction is the same
    #   the row/col is the same
    #   the col/row differs by 1

    # union find or subgraphs to create the sides (groups of perimeter units)

    # Using a graph where a node is a unit of perimeter
    # and an edge means they are on the same side and adjacent.
    # Tarjan's will give us the subgraphs (i.e. a side)
    # Number of sides = Number of subgraphs

    pd_set = get_perimeter_points(plot)
    gph = {}
    for u in pd_set:
        gph[u] = {}
        for v in pd_set:
            if u == v:
                continue
            # adjacent on a row
            if u[0][0] == v[0][0] and abs(u[0][1] - v[0][1]) == 1 and u[1] == v[1]:
                gph[u][v] = 1
                continue
            # adjacent on a column
            if u[0][1] == v[0][1] and abs(u[0][0] - v[0][0]) == 1 and u[1] == v[1]:
                gph[u][v] = 1
                continue
    sgs = tarjan(gph)
    return len(sgs)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    sz, grid = data
    plots = get_plots(sz, grid)
    ans = 0
    for plot in plots:
        ans += len(plot) * get_sides(plot)
    return ans


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
