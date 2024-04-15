"""Advent of code 2015
--- Day 5: Doesn't He Have Intern-Elves For This? ---
"""

from itertools import pairwise
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import window_over


def parse_data(raw_data):
    """Parse the input"""
    data = raw_data
    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    nice = 0
    for s in data:

        if "ab" in s or "cd" in s or "pq" in s or "xy" in s:
            continue

        v_cnt = 0
        for ch in s:
            if ch in "aeiou":
                v_cnt += 1

        if v_cnt < 3:
            continue

        pair = False
        for a, b in pairwise(s):
            if a == b:
                pair = True
                break
        if not pair:
            continue

        nice += 1

    return nice


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    nice = 0
    for s in data:
        rpt_a = False
        for i, a in enumerate(window_over(s, 2)):
            if a in s[:i] or a in s[i + 2 :]:
                rpt_a = True
                break

        rpt_b = False
        for a in window_over(s, 3):
            if a[0] == a[2]:
                rpt_b = True
                break

        if rpt_a and rpt_b:
            nice += 1

    return nice


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
