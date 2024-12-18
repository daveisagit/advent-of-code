"""Advent of code 2024
--- Day 18: RAM Run ---
"""

import re
from common.aoc import file_to_list, aoc_part, get_filename
from common.graph import dijkstra, reachable
from common.grid_2d import make_blank_grid, make_graph_from_grid


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        sr = re.search(r"(\d+),+(\d+)", line)
        d = tuple(int(g) for g in sr.groups())
        data.append(d)
    return data


def get_grid(sz, data, limit):
    """Apply the locations of the bad memory"""
    grid = make_blank_grid(sz, sz)
    for p in data[:limit]:
        grid[p] = "#"
    return grid


@aoc_part
def solve_part_a(data, sz=7, limit=12) -> int:
    """Solve part A"""
    grid = get_grid(sz, data, limit)
    start = 0, 0
    target = sz - 1, sz - 1
    gph = make_graph_from_grid(grid)
    dst = dijkstra(gph, start, target, weight_attr=None)
    return dst


@aoc_part
def solve_part_b(data, sz=7, limit=12) -> int:
    """Solve part B"""
    grid = get_grid(sz, data, limit)
    start = 0, 0
    target = sz - 1, sz - 1
    gph = make_graph_from_grid(grid)

    for u in data[limit:]:
        vs = {v for v in gph[u]}
        for v in vs:
            del gph[u][v]
            del gph[v][u]
        r = reachable(gph, start)
        if target not in r:
            return u

    return len(data)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA, sz=71, limit=1024)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA, sz=71, limit=1024)
