"""Advent of code 2016
--- Day 24: Air Duct Spelunking ---
"""

from operator import add

from common.aoc import file_to_list, aoc_part, get_filename
from common.grid_2d import directions, maze_to_graph
from common.graph import optimal_route, simplify


def parse_data_old(raw_data):
    """Parse the input"""
    gph = {}
    poi = {}
    for r, line in enumerate(raw_data):
        for c, ch in enumerate(line):
            if ch == "#":
                continue
            p = (r, c)
            if ch.isdigit():
                poi[p] = ch
            gph[p] = {}

    nodes = set(gph)
    for u in nodes:
        for d in directions.values():
            v = tuple(map(add, u, d))
            if v in nodes:
                gph[u][v] = 1
                gph[v][u] = 1

    simplify(gph, poi)

    return gph, poi


def parse_data(raw_data):
    """Parse the input"""
    mz = {}
    poi = {}
    start = None
    for r, line in enumerate(raw_data):
        for c, ch in enumerate(line):
            if ch == "#":
                continue
            p = (r, c)
            if ch.isdigit():
                poi[p] = ch
                start = p
            mz[p] = ch

    gph = maze_to_graph(start, mz, path_char=".", node_chars="0123456789")

    return gph, poi


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    gph, poi = data
    start = [p for p, n in poi.items() if n == "0"][0]
    visit = {p for p, n in poi.items() if n != "0"}
    opt_route = optimal_route(gph, visit, start=start)
    return opt_route[0]


# Part B - Alternative (all perms as it is circular)
# @aoc_part
# def solve_part_b(data) -> int:
#     """Solve part B"""
#     gph, poi = data

#     visit = {p for p, n in poi.items()}
#     am = get_adjacency_matrix(gph, visit)
#     best = inf
#     for p in permutations(visit):
#         p = list(p)
#         p.append(p[0])
#         cost = sum(am[a][b] for a, b in pairwise(p))
#         best = min(best, cost)
#     return best


@aoc_part
def solve_part_b(data) -> int:
    """Solve part A"""
    gph, poi = data
    start = [p for p, n in poi.items() if n == "0"][0]
    visit = {p for p, n in poi.items() if n != "0"}
    opt_route = optimal_route(gph, visit, start=start, end=start)
    return opt_route[0]


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
