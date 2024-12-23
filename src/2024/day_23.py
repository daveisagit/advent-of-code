"""Advent of code 2024
--- Day 23: LAN Party ---
"""

import re

from collections import defaultdict
from heapq import heappop, heappush
from itertools import combinations

from common.aoc import file_to_list, aoc_part, get_filename
from common.graph import all_nodes, bron_kerbosch


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        sr = re.search(r"(..)-(..)", line)
        d = tuple(g for g in sr.groups())
        data.append(d)
    return data


def make_graph(data):
    gph = defaultdict(dict)
    for u, v in data:
        gph[u][v] = 1
        gph[v][u] = 1
    return gph


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    gph = make_graph(data)
    cnt = 0
    nodes = all_nodes(gph)
    for cmb in combinations(nodes, 3):
        u, v, w = cmb
        if u in gph and v in gph and w in gph:
            if v in gph[u] and w in gph[v] and u in gph[w]:
                if "t" in u[0] or "t" in v[0] or "t" in w[0]:
                    cnt += 1

    return cnt


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    gph = make_graph(data)
    h = []
    # state = -ve length, nodes of the current K-graph
    nodes = all_nodes(gph)
    for n in nodes:
        state = -1, frozenset({n})
        heappush(h, state)
    seen = set()
    best = 0
    best_set = None
    while h:
        state = heappop(h)
        l, fs = state
        if fs in seen:
            continue
        seen.add(fs)

        # check if target reached
        if len(fs) > best:
            best = len(fs)
            best_set = fs
            print(best_set)

        # add options to heap
        available = nodes - fs
        for v in available:
            if all(u in gph[v] for u in fs):
                nfs = frozenset(fs | {v})
                new_state = -len(fs), nfs
                heappush(h, new_state)

    s = ",".join(sorted(best_set))
    return s


@aoc_part
def solve_part_c(data) -> int:
    """Solve part B - using bron_kerbosch"""
    gph = make_graph(data)
    N = all_nodes(gph)
    max_clique = 0
    for clq in bron_kerbosch(gph, N):
        if len(clq) > max_clique:
            max_clique = len(clq)
            ans = clq
    s = ",".join(sorted(ans))
    return s


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
# quite slow - better to use bron_kerbosch see part_c
# solve_part_b(MY_DATA)
solve_part_c(MY_DATA)
