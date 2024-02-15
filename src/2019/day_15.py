"""Advent of code 2019
--- Day 15: Oxygen System ---
"""

from collections import defaultdict, deque
from copy import deepcopy
from operator import add
from common.aoc import aoc_part, file_to_string, get_filename
from common.graph import dijkstra, simplify
from common.grid_2d import directions, get_grid_limits
from common.intcode import IntCode

NEWS = {
    ">": 4,
    "^": 1,
    "<": 3,
    "v": 2,
}


def draw_map(seen, oxygen):
    """Visualize"""
    min_x, min_y, max_x, max_y = get_grid_limits(seen)
    width = max_x - min_x + 1
    for r in range(min_y, max_y + 1):
        row = [" "] * width
        for ic, c in enumerate(range(min_x, max_x + 1)):
            if (r, c) in seen:
                row[ic] = "."
            if (r, c) == oxygen:
                row[ic] = "O"
            if (r, c) == (0, 0):
                row[ic] = "S"
        print("".join(row))
    print()


def create_map(data):
    """Explore all avenues, create a map"""
    m = defaultdict(dict)  # graph of steps
    ic = IntCode(data)
    origin = (0, 0)
    bfs = deque()
    bfs.append((origin, ic))
    seen = set()
    oxygen = None
    while bfs:
        pos, ic = bfs.popleft()
        if pos in seen:
            continue
        seen.add(pos)

        for k, d in directions.items():
            nxt_pos = tuple(map(add, pos, d))
            if nxt_pos in seen:
                continue

            nic = deepcopy(ic)
            nic.input.append(NEWS[k])
            nic.go()
            reply = nic.output.pop()

            if reply == 0:
                continue
            if reply == 2:
                oxygen = nxt_pos

            m[pos][nxt_pos] = 1
            m[nxt_pos][pos] = 1

            bfs.append((nxt_pos, nic))

    return seen, m, oxygen


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    seen, m, oxygen = data
    draw_map(seen, oxygen)
    simplify(m)
    r = dijkstra(m, (0, 0), oxygen)
    return r


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    _, m, oxygen = data
    simplify(m)
    r = dijkstra(m, oxygen, None)
    return max(r.values())


MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = create_map(MY_RAW_DATA)

solve_part_a(MY_DATA)
solve_part_b(MY_DATA)
