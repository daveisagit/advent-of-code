"""Advent of code 2023
--- Day 17: Clumsy Crucible ---
"""

from collections import defaultdict
from operator import add
from common.aoc import file_to_list, aoc_part, get_filename
from common.graph import dijkstra
from common.grid_2d import directions


def parse_data(raw_data):
    """Return the heat map"""
    heat_map = {}
    for ri, row in enumerate(raw_data):
        for ci, content in enumerate(row):
            hl = int(content)
            p = (ri, ci)
            heat_map[p] = hl

    max_r = len(raw_data)
    max_c = len(raw_data[0])

    return max_r, max_c, heat_map


def make_graph(max_r, max_c, heat_map, source, target, min_move=1, max_move=3):
    """Return a directed graph where
    a node = ( pos , direction , distance travelled in that direction )
    an edge = the heat loss moving into the target location
    We can only turn left/right/straight and must turn after max_moves
    We must go straight for at least min_moves
    """
    gph = defaultdict(dict)

    # there are 2 ways to start moving, cost is dependent
    for d in directions.values():
        if any(x < 0 for x in d):
            continue
        u = (d, d, 1)
        gph[source][u] = heat_map[d]

    # there are many ways to finish, but they cost nothing
    for d in directions.values():
        for m in range(min_move, max_move + 1):
            u = (target, d, m)
            gph[u][target] = 0

    # create nodes and edges
    for r in range(max_r):
        for c in range(max_c):
            for d in directions.values():
                for m in range(1, max_move + 1):

                    # for each possible direction out from this location
                    for ed in directions.values():

                        # reversing not allowed
                        if tuple(map(add, d, ed)) == (0, 0):
                            continue

                        # only straight ahead allowed, if not made the minimum moves
                        if m < min_move and d != ed:
                            continue

                        if d == ed:
                            # same direction, check not over the max
                            if m == max_move:
                                continue
                            # ok, increment
                            vm = m + 1
                        else:
                            # changed direction, reset count
                            vm = 1

                        # get next location and ensure it is in the map
                        p = (r, c)
                        q = tuple(map(add, p, ed))
                        if q not in heat_map:
                            continue

                        # create the edge
                        u = (p, d, m)
                        v = (q, ed, vm)
                        gph[u][v] = heat_map[q]

    return gph


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    max_r, max_c, heat_map = data
    source = (0, 0)
    target = (max_r - 1, max_c - 1)
    gph = make_graph(max_r, max_c, heat_map, source, target)
    return dijkstra(gph, source, target)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    max_r, max_c, heat_map = data
    source = (0, 0)
    target = (max_r - 1, max_c - 1)
    gph = make_graph(max_r, max_c, heat_map, source, target, min_move=4, max_move=10)
    return dijkstra(gph, source, target)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
