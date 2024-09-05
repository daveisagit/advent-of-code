"""Advent of code 2020
--- Day 13: Shuttle Search ---
"""

from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok
from common.numty import solve_congruences


def parse_data(raw_data):
    """Parse the input"""
    est = int(raw_data[0])
    bid = tok(raw_data[1], ",")
    return est, bid


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    est, bid = data
    bid = [int(v) for v in bid if v != "x"]
    wait = [(i, v - (est % v)) for i, v in enumerate(bid)]
    wait = sorted(wait, key=lambda x: x[1])
    least_wait = wait[0]
    return least_wait[1] * bid[least_wait[0]]


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    _, bid = data
    non_x = [int(v) for v in bid if v != "x"]
    cong = []
    for bus in non_x:
        idx = bid.index(str(bus))
        cong.append((-idx, bus))

    return solve_congruences(cong)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
