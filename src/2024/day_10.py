"""Advent of code 2024
--- Day 10: Hoof It ---
"""

from collections import deque, defaultdict
from functools import lru_cache
from operator import add

from common.aoc import (
    file_to_list,
    aoc_part,
    get_filename,
)
from common.graph import find_all_paths, get_adjacency_matrix
from common.grid_2d import directions


def parse_data(raw_data):
    """Parse the input"""
    grid = {}
    zeros = set()
    nines = set()
    for ri, row in enumerate(raw_data):
        for ci, ch in enumerate(row):
            p = (ri, ci)
            grid[p] = int(ch)
            if ch == "0":
                zeros.add(p)
            if ch == "9":
                nines.add(p)

    return grid, zeros, nines


def make_graph(grid: dict, zeros: set) -> defaultdict:
    """Return a graph of trails"""

    gph = defaultdict(dict)

    bfs = deque()
    seen = set()
    for p in zeros:
        bfs.append(p)

    while bfs:
        p = bfs.popleft()
        if p in seen:
            continue
        seen.add(p)

        h = grid[p]
        if h == 9:
            continue

        for dv in directions.values():
            np = tuple(map(add, p, dv))

            if np not in grid:
                continue

            nh = grid[np]
            if nh != h + 1:
                continue

            gph[p][np] = 1
            bfs.append(np)

    return gph


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    grid, zeros, nines = data
    gph = make_graph(grid, zeros)
    nodes = zeros | nines
    am = get_adjacency_matrix(gph, nodes)
    cnt = 0
    for r in am.values():
        for x in r.values():
            if x == 9:
                cnt += 1

    return cnt


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    grid, zeros, nines = data
    gph = make_graph(grid, zeros)
    nodes = zeros | nines
    am = get_adjacency_matrix(gph, nodes)
    cnt = 0
    for u, r in am.items():
        for v, x in r.items():
            if x == 9:
                paths = find_all_paths(gph, u, v)
                cnt += len(paths)

    return cnt


@aoc_part
def solve_part_c(data) -> int:
    """Solve part C
    No need to graph
    Just a simple BFS for collecting all the unique trails
    There won't be any cycles given the ascending trail
    """
    grid, zeros, _ = data
    bfs = deque()
    for p in zeros:
        bfs.append((p,))

    trails = []

    while bfs:
        trail = bfs.popleft()
        head = trail[-1]
        h = grid[head]
        if h == 9:
            trails.append(trail)
            continue

        for dv in directions.values():
            new_head = tuple(map(add, head, dv))

            if new_head not in grid:
                continue

            nh = grid[new_head]
            if nh != h + 1:
                continue

            bfs.append(trail + (new_head,))

    # set of heads and tails
    hat = {(t[0], t[9]) for t in trails}
    print(f"A: {len(hat)}")
    print(f"B: {len(trails)}")


@aoc_part
def solve_part_d(data) -> int:
    """Solve
    Using recursion and memoize the trails from a given point
    """

    @lru_cache(maxsize=None)
    def trails_from(p):
        trails = []
        if grid[p] == 9:
            trails.append((p,))
            return trails

        for dv in directions.values():
            np = tuple(map(add, p, dv))
            if np not in grid:
                continue
            if grid[np] != grid[p] + 1:
                continue
            for trail in trails_from(np):
                trails.append((p,) + trail)
        return tuple(trails)

    grid, zeros, _ = data

    all_trails = []
    for z in zeros:
        all_trails.extend(trails_from(z))

    # set of heads and tails
    hat = {(t[0], t[9]) for t in all_trails}
    print(f"A: {len(hat)}")
    print(f"B: {len(all_trails)}")


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)


MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)

solve_part_c(MY_DATA)
solve_part_d(MY_DATA)
