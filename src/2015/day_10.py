"""Advent of code 2015
--- Day 10: Elves Look, Elves Say ---
"""

from common.aoc import file_to_string, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    data = raw_data
    return data


def next_seq(s):
    """Look and say"""
    new_seq = ""
    stk = []
    for p in range(len(s) + 1):
        if p == len(s) or stk and stk[-1] != s[p]:
            new_seq += str(len(stk)) + stk[-1]
            stk.clear()

        if p != len(s):
            stk.append(s[p])

    return new_seq


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    s = data
    for _ in range(40):
        s = next_seq(s)
    return len(s)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    s = data
    for _ in range(50):
        s = next_seq(s)
    return len(s)


MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(MY_DATA)

solve_part_b(MY_DATA)
