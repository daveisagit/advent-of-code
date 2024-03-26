"""Advent of code 2018
--- Day 22: Mode Maze ---
Part B could be faster if made the graph in a lazy fashion due to the 
unknown boundary
"""

from collections import defaultdict
from operator import add
from common.aoc import aoc_part
from common.graph import dijkstra
from common.grid_2d import directions


def get_erosion_levels(target, depth, scan=None):
    """Return erosion levels"""
    data = {}
    if scan is None:
        scan = target
    for y in range(scan[0] + 1):
        for x in range(scan[1] + 1):
            p = (y, x)
            if p in ((0, 0), target):
                gi = 0
                el = (gi + depth) % 20183
                data[p] = (gi, el)
                continue
            if y == 0:
                gi = x * 16807
                el = (gi + depth) % 20183
                data[p] = (gi, el)
                continue
            if x == 0:
                gi = y * 48271
                el = (gi + depth) % 20183
                data[p] = (gi, el)
                continue

            gi = data[(y - 1, x)][1] * data[(y, x - 1)][1]
            el = (gi + depth) % 20183
            data[p] = (gi, el)

    return data


def draw(target, erosion_levels, margin=0, marker=None):
    """Visual"""
    ch_map = [".", "=", "|"]

    for y in range(target[1] + 1 + margin):
        row = ""
        for x in range(target[0] + 1 + margin):
            ch = " "
            p = (y, x)
            if p == (0, 0):
                ch = "M"
            elif p == target:
                ch = "T"
            elif marker and p == marker[0]:
                ch = str(marker[1])
            else:
                ch = ch_map[erosion_levels[p][1] % 3]
            row += ch
        print(row)


def risk(target, erosion_levels):
    """Risk Assessment"""
    ra = 0
    for y in range(target[0] + 1):
        for x in range(target[1] + 1):
            p = (y, x)
            ra += erosion_levels[p][1] % 3
    return ra


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    depth, target = data
    target = (target[1], target[0])
    el = get_erosion_levels(target, depth)
    return risk(target, el)


def get_terrain(erosion_levels):
    """Terrain values"""
    return {pos: el[1] % 3 for pos, el in erosion_levels.items()}


def make_graph(terrain):
    """All routes
    NOTHING = 0
    TORCH = 1
    GEAR = 2
    """
    valid_terrain = ((1, 2), (0, 2), (0, 1))
    gph = defaultdict(dict)

    for pos, ct in terrain.items():
        for eq in range(3):
            cur_state = (pos, eq)

            if ct not in valid_terrain[eq]:
                continue

            for d in directions.values():
                nxt = tuple(map(add, pos, d))
                nxt_state = (nxt, eq)
                if nxt in terrain:
                    if terrain[nxt] in valid_terrain[eq]:
                        gph[cur_state][nxt_state] = 1
                        continue

            for eq2 in range(3):
                if eq2 == eq:
                    continue
                if ct not in valid_terrain[eq2]:
                    continue
                nxt_state = (pos, eq2)
                gph[cur_state][nxt_state] = 7

    return gph


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    depth, target = data
    target = (target[1], target[0])
    margin = max(target)
    scan = tuple(map(add, target, (margin, margin)))
    el = get_erosion_levels(target, depth, scan=scan)
    terrain = get_terrain(el)
    gph = make_graph(terrain)
    print(f"Graph made {len(gph)}")
    sp = dijkstra(gph, ((0, 0), 1), (target, 1))
    return sp


EX_DATA = 510, (10, 10)
MY_DATA = 11991, (6, 797)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
