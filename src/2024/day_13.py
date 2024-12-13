"""Advent of code 2024
--- Day 13: Claw Contraption ---
"""

import re

from common.aoc import (
    file_to_list,
    aoc_part,
    get_filename,
)
from common.general import input_sections
from common.linear_algebra import mtx_solve


def parse_data(raw_data):
    """Parse the input"""
    # Button A: X+69, Y+23
    # Button B: X+27, Y+71
    # Prize: X=18641, Y=10279
    data = []
    for sec in input_sections(raw_data):
        s = []
        for line in sec:
            sr = re.search(r".+:\sX(?:\+|=)(\d+),\sY(?:\+|=)(\d+)", line)
            d = tuple(int(g) for g in sr.groups())
            s.append(d)
        data.append(s)
    return data


def solve(data, part_b_amount=0) -> int:
    """Solve"""

    # Button A: Ax, Ay
    # Button B: Bx, By
    # Prize   : Px, Py

    # let (a,b) be the number of presses of each button

    # a.Ax + b.Bx = Px
    # a.Ay + b.By = Py

    # |Ax  Bx| . |a| = |Px|
    # |Ay  By|   |b|   |Py|

    # Seems finding the minimum presses for A is a deliberate red-herring
    # given there can only be 1 solution or no solution

    # if the only solution is non-integer then ignore

    total = 0
    for d in data:
        Ax = d[0][0]
        Ay = d[0][1]

        Bx = d[1][0]
        By = d[1][1]

        Px = d[2][0]
        Py = d[2][1]

        mtx = [
            [Ax, Bx],
            [Ay, By],
        ]

        try:
            # non integer solutions and no solution raise an exception
            # which we can ignore
            res = mtx_solve(
                mtx, (Px + part_b_amount, Py + part_b_amount), expect_integer=True
            )
            assert res[0] == 1
            amt_A = res[1][0]
            amt_B = res[1][1]
            total += amt_A * 3 + amt_B
        except:
            pass

    return total


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    return solve(data)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    return solve(data, part_b_amount=10000000000000)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
