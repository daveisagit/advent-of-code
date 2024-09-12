"""Advent of code 2023
--- Day 25: Snowverload ---
"""

from collections import defaultdict
import sys
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok
from common.graph import stoer_wagner, tarjan, which_edges_wagner


def parse_data(raw_data):
    """Parse the input"""

    gph = defaultdict(dict)
    for line in raw_data:
        u = line[:3]
        for v in tok(line[4:]):
            if not v:
                continue
            gph[u][v] = 1
            gph[v][u] = 1
    return gph


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    min_cut, (sg1, sg2) = stoer_wagner(data)
    print(f"Minimum cut={min_cut}")

    sys.setrecursionlimit(2000)
    assert len(tarjan(data)) == 1

    # cut the edges to test tarjan
    to_cut = which_edges_wagner(data, sg1, sg2)
    for u, v in to_cut:
        del data[u][v]
        del data[v][u]
    sub_graphs = tarjan(data)
    assert len(sub_graphs) == 2
    tsg1 = set(sub_graphs[0])
    tsg2 = set(sub_graphs[1])
    assert sg1 == tsg1 or sg1 == tsg2
    assert sg2 == tsg1 or sg2 == tsg2

    return len(sg1) * len(sg2)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)
