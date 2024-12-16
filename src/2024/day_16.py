"""Advent of code 2024
--- Day 16: Reindeer Maze ---
"""

from collections import defaultdict
from heapq import heappop, heappush
from itertools import count
from operator import add


from common.aoc import (
    file_to_list,
    aoc_part,
    get_filename,
)
from common.graph import dijkstra, dijkstra_all_paths
from common.grid_2d import (
    list_2d_to_dict,
    rotations,
)


def parse_data(raw_data):
    """Parse the input"""
    sz, grid, poi = list_2d_to_dict(
        raw_data, poi_labels="SE", replace_poi_with_char="."
    )
    start = poi["S"]
    target = poi["E"]
    return grid, sz, start, target


def get_best_path_score(data):
    """Return the best score attainable"""
    grid, sz, start, target = data
    h = []
    # state = (score, pos, direction)
    state = 0, start, 0
    heappush(h, state)
    seen = set()
    while h:
        score, pos, d = heappop(h)
        if (pos, d) in seen:
            continue
        seen.add((pos, d))

        # check if target reached
        if pos == target:
            return score

        # add options to heap
        dv = rotations[d]
        np = tuple(map(add, pos, dv))

        if pos in grid and grid[pos] == ".":
            state = score + 1, np, d
            heappush(h, state)

        for t in (-1, 1):
            nd = (d + t) % 4
            np = tuple(map(add, pos, rotations[nd]))
            if np in grid and grid[np] == ".":
                state = score + 1000, pos, nd
                heappush(h, state)


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    return get_best_path_score(data)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    # this time keep path in state
    # (score, path, direction)
    # if we match best score then add path to seats
    score_best_path = get_best_path_score(data)
    grid, sz, start, target = data
    h = []
    state = 0, (start,), 0
    heappush(h, state)
    seats = set()
    best_score_at = {}
    while h:
        score, pth, d = heappop(h)
        pos = pth[-1]
        if (pos, d) in best_score_at:
            if score > best_score_at[(pos, d)]:
                continue
        best_score_at[(pos, d)] = score

        if score > score_best_path:
            break

        if pos == target:
            if score == score_best_path:
                seats |= set(pth)
            continue

        # add options to heap
        dv = rotations[d]
        np = tuple(map(add, pos, dv))

        if pos in grid and grid[pos] == ".":
            state = score + 1, pth + (np,), d
            heappush(h, state)

        for t in (-1, 1):
            nd = (d + t) % 4
            np = tuple(map(add, pos, rotations[nd]))
            if np in grid and grid[np] == ".":
                state = score + 1000, pth, nd
                heappush(h, state)

    return len(seats)


def make_graph(data):
    """Alternative approach by including direction we are facing in the
    state = node"""
    gph = defaultdict(dict)
    grid, sz, start, target = data
    for r in range(sz[0]):
        for c in range(sz[1]):
            p = (r, c)
            for f, fv in enumerate(rotations):
                u = (p, f)

                # move
                np = tuple(map(add, p, fv))
                if np in grid and grid[np] == ".":
                    v = (np, f)
                    gph[u][v] = 1

                # left
                nf = (f + 1) % 4
                np = tuple(map(add, p, rotations[nf]))
                if np in grid and grid[np] == ".":
                    v = (p, nf)
                    gph[u][v] = 1000

                # right
                nf = (f - 1) % 4
                np = tuple(map(add, p, rotations[nf]))
                if np in grid and grid[np] == ".":
                    v = (p, nf)
                    gph[u][v] = 1000

    for f in range(4):
        u = (target, f)
        gph[u][target] = 0
        gph[target][u] = 0

    return gph


@aoc_part
def solve_part_c(data) -> int:
    """Solve using a graph with facing direction in state/node
    This provoked the creation of dijkstra_all_paths which is a tweak
    of dijkstra_paths with a <= instead < and a list of paths instead of just 1.
    """
    grid, sz, start, target = data
    gph = make_graph(data)
    dst = dijkstra(gph, (start, 0), target)
    _, all_paths = dijkstra_all_paths(gph, (start, 0), target)
    ps = {p for pth in all_paths for p, _ in pth}
    # take off 1 because of the fake target node with no direction
    return dst, len(ps) - 1


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)

solve_part_c(EX_DATA)
solve_part_c(MY_DATA)
