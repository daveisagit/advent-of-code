"""Advent of code 2019
--- Day 20: Donut Maze ---
"""

from collections import defaultdict
from operator import add
from common.aoc import ENCODING, aoc_part, get_filename
from common.grid_2d import directions
from common.graph import simplify, dijkstra


def parse_data(raw_data):
    """Parse the input, return the maze points, portals as internal/external ports"""

    def get_portals():
        portal = defaultdict(set)
        internal = {}
        external = {}
        width = len(grid[0])
        for ri, row in enumerate(grid[2:-2]):

            name = ("".join(row[:2])).strip()
            if name:
                portal[name].add((ri, 0))
                external[name] = (ri, 0)

            name = ("".join(row[donut_width + 2 : donut_width + 4])).strip()
            if name and name.isalpha():
                portal[name].add((ri, donut_width - 1))
                internal[name] = (ri, donut_width - 1)

            name = ("".join(row[-(donut_width + 4) : -(donut_width + 2)])).strip()
            if name and name.isalpha():
                portal[name].add((ri, width - 4 - donut_width))
                internal[name] = (ri, width - 4 - donut_width)

            name = ("".join(row[-2:])).strip()
            if name:
                portal[name].add((ri, width - 5))
                external[name] = (ri, width - 5)

        return portal, external, internal

    grid = []
    cnt = 0
    longest_stretch_of_spaces = 0
    for line in raw_data[2:-2]:
        row = list(line)[2:-2]
        for c in row:
            if c == " ":
                if cnt:
                    cnt += 1
                else:
                    cnt = 1
            else:
                longest_stretch_of_spaces = max(cnt, longest_stretch_of_spaces)
                cnt = 0

    grid = []
    for line in raw_data:
        row = list(line)[:-1]
        grid.append(row)

    donut_width = (len(grid[0]) - 4 - longest_stretch_of_spaces) // 2

    portals = defaultdict(set)
    h_ports, external, internal = get_portals()
    for k, ps in h_ports.items():
        for p in ps:
            portals[k].add(p)

    # transpose to get the vertical ports
    grid = list(map(list, zip(*grid)))
    v_ports, v_external, v_internal = get_portals()
    for k, ps in v_ports.items():
        for p in ps:
            portals[k].add((p[1], p[0]))
    for k, p in v_external.items():
        external[k] = (p[1], p[0])
    for k, p in v_internal.items():
        internal[k] = (p[1], p[0])

    maze_points = set()
    for ri, line in enumerate(raw_data[2:-2]):
        for ci, c in enumerate(line[2:-2]):
            if c == ".":
                maze_points.add((ri, ci))

    return maze_points, portals, external, internal


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    maze_points, portals, _, _ = data
    maze_graph = defaultdict(dict)
    for p in maze_points:
        for d in directions.values():
            n = tuple(map(add, p, d))
            if n in maze_points:
                maze_graph[p][n] = 1
                maze_graph[n][p] = 1

    for ps in portals.values():
        if len(ps) != 2:
            continue
        pl = list(ps)
        pa = pl[0]
        pb = pl[1]
        maze_graph[pa][pb] = 1
        maze_graph[pb][pa] = 1

    simplify(maze_graph)

    start = list(portals["AA"])[0]
    target = list(portals["ZZ"])[0]
    sp = dijkstra(maze_graph, start, target=target)
    return sp


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""

    def create_level():
        for u, n in base.items():
            for v, d in n.items():
                maze[(level, u)][(level, v)] = d
                maze[(level, v)][(level, u)] = d
        if level > 0:
            for k, p in external.items():
                if k in internal:
                    in_n = (level - 1, internal[k])
                    ex_n = (level, p)
                    maze[in_n][ex_n] = 1
                    maze[ex_n][in_n] = 1
        simplify(maze)

    maze_points, portals, external, internal = data
    start = (0, list(portals["AA"])[0])
    target = (0, list(portals["ZZ"])[0])
    maze = defaultdict(dict)

    base = defaultdict(dict)
    for p in maze_points:
        for d in directions.values():
            n = tuple(map(add, p, d))
            if n in maze_points:
                base[p][n] = 1
                base[n][p] = 1
    simplify(base)

    best = None
    level = -1
    while True:
        level += 1
        create_level()
        sp = dijkstra(maze, start, target=target)
        if sp:
            if best is None or sp < best:
                best = sp
                continue
            if sp == best:
                print(f"{level} levels deep")
                return sp


with open(get_filename(__file__, "ex"), encoding=ENCODING) as f:
    EX_RAW_DATA = f.readlines()
EX_DATA = parse_data(EX_RAW_DATA)

with open(get_filename(__file__, "my"), encoding=ENCODING) as f:
    MY_RAW_DATA = f.readlines()
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
