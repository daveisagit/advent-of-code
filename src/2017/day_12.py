"""Advent of code 2017
--- Day 12: Digital Plumber ---
"""

from collections import defaultdict, deque
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok
from common.graph import tarjan


def parse_data(raw_data):
    """Parse the input"""
    gph = defaultdict(dict)
    for line in raw_data:
        arr = tok(line, "<->")
        pid = int(arr[0])
        com = [int(p) for p in tok(arr[1], ",")]
        for p in com:
            gph[pid][p] = 1
            gph[p][pid] = 1
    return gph


def same_group(gph, p):
    """Return a set of IDs in the same group"""
    bfs = deque()
    bfs.append(p)
    seen = set()
    while bfs:
        p = bfs.popleft()
        if p in seen:
            continue
        seen.add(p)
        for q in gph[p]:
            bfs.append(q)
    return seen


@aoc_part
def solve_part_a(gph) -> int:
    """Solve part A"""
    sg = same_group(gph, 0)
    return len(sg)


@aoc_part
def solve_part_b(gph) -> int:
    """Solve part B"""
    all_pgm = set(gph)
    grp_cnt = 0
    while all_pgm:
        a = list(all_pgm)[0]
        sg = same_group(gph, a)
        grp_cnt += 1
        all_pgm.difference_update(sg)

    return grp_cnt


@aoc_part
def solve_part_c(gph) -> int:
    """Solve both parts with Tarjan algorithm"""
    # get a list subgraphs, each subgraph is a list of nodes
    cgs = tarjan(gph)
    for scc in cgs:
        if 0 in scc:
            print(len(scc))
    return len(cgs)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)

solve_part_c(MY_DATA)
