"""Advent of code 2024
--- Day 7: Bridge Repair ---
"""

from itertools import product

from common.aoc import (
    file_to_list,
    aoc_part,
    get_filename,
)
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        arr = tok(line, ":")
        t = int(arr[0])
        arr = tok(arr[1])
        vs = tuple(int(v) for v in arr)
        eq = t, vs
        data.append(eq)
    return data


def passes_a(t: int, vs: tuple) -> bool:
    all_ops = product(["+", "*"], repeat=len(vs) - 1)
    for ops in all_ops:
        s = vs[0]
        for i, x in enumerate(vs[1:]):
            if ops[i] == "*":
                s *= x
            else:
                s += x
        if s == t:
            return True
    return False


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    s = 0
    for t, vs in data:
        if passes_a(t, vs):
            s += t
    return s


def passes_b(t: int, vs: tuple) -> bool:
    all_ops = product(["+", "*", "|"], repeat=len(vs) - 1)
    for ops in all_ops:
        s = vs[0]
        for i, x in enumerate(vs[1:]):
            if ops[i] == "*":
                s *= x
            elif ops[i] == "+":
                s += x
            else:
                s = int(str(s) + str(x))
            # this comparison does not seem to improve time
            # if s > t:
            #     break
        if s == t:
            return True
    return False


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    s = 0
    for t, vs in data:
        if passes_b(t, vs):
            s += t
    return s


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
