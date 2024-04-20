"""Advent of code 2015
--- Day 23: Opening the Turing Lock ---
"""

from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        arr = tok(line, ",")
        arr2 = tok(arr[0])
        op = arr2[0]
        arg = arr2[1]
        jx = None
        if len(arr) > 1:
            jx = int(arr[1])
        if arg not in ("a", "b"):
            arg = int(arg)

        t = (op, arg, jx)
        data.append(t)

    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    return len(data)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    return len(data)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
