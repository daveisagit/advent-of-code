"""Advent of code 2022
--- Day 10: Cathode-Ray Tube ---
"""

from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    pgm = []
    for line in raw_data:
        arr = tok(line)
        step = len(arr), arr[0], int(arr[1]) if len(arr) > 1 else None
        pgm.append(step)
    return pgm


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    x = [1]
    for _, op, v in data:
        x.append(x[-1])
        if op == "addx":
            x.append(x[-1] + v)
    return sum((idx * 40 + 20) * v for idx, v in enumerate(x[19:229:40]))


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    x = [1]
    for _, op, v in data:
        x.append(x[-1])
        if op == "addx":
            x.append(x[-1] + v)

    for r in range(6):
        line = ""
        for c in range(40):
            p = r * 40 + c
            if x[p] - 1 <= c <= x[p] + 1:
                line += "#"
            else:
                line += "."
        print(line)

    return None


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
