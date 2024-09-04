"""Advent of code 2023
--- Day 25: Snowverload ---
"""

from collections import defaultdict
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok
from common.graph import stoer_wagner


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
    return len(sg1) * len(sg2)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)
