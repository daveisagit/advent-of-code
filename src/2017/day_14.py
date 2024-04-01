"""Advent of code 2017
--- Day 14: Disk Defragmentation ---
"""

from collections import Counter, defaultdict
from operator import add
from common.aoc import aoc_part, file_to_string, get_filename
from common.general import window_over
from common.graph import subgraph_nodes
from common.grid_2d import grid_lists_to_dict, directions


def parse_data(raw_data):
    """Parse the input"""
    data = raw_data
    return data


def knot_hash(s):
    """Hash Man!"""

    def knot_twist():
        nonlocal cp, skip, lst, data
        for l in data:
            for i in range(((l + 1) // 2)):
                i1 = (cp + i) % sz
                i2 = (cp - i + l - 1) % sz
                lst[i1], lst[i2] = lst[i2], lst[i1]
            cp += l + skip
            skip += 1

    lst = list(range(256))
    data = [ord(c) for c in s]
    data += [17, 31, 73, 47, 23]
    sz = len(lst)
    cp = 0
    skip = 0
    for _ in range(64):
        knot_twist()

    dense = []
    for block in window_over(lst, 16, 16):
        c = block[0]
        for d in block[1:]:
            c ^= d
        dense.append(c)

    return dense


def dense_to_bin(dense):
    """return dense hash as binary string"""
    return "".join([f"{d:08b}" for d in dense])


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    s = ""
    for x in range(128):
        dense = knot_hash(f"{data}-{x}")
        b = dense_to_bin(dense)
        s += b

    cnt = Counter(s)
    return cnt["1"]


def grid_to_graph(grid):
    """Return an undirected graph of the connect 1s"""
    gph = defaultdict(dict)
    for u, content in grid.items():
        if content == "0":
            continue
        gph[u] = {}
        for d in directions.values():
            v = tuple(map(add, u, d))
            if grid.get(v, "0") == "1":
                gph[u][v] = 1
                gph[v][u] = 1
    return gph


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    grid = []
    for x in range(128):
        dense = knot_hash(f"{data}-{x}")
        grid.append(list(dense_to_bin(dense)))

    grid = grid_lists_to_dict(grid)
    gph = grid_to_graph(grid)
    sgn = subgraph_nodes(gph)
    return len(sgn)


EX_RAW_DATA = file_to_string(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
