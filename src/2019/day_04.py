"""Advent of code 2019
--- Day 4: Secure Container ---
"""

from common.aoc import aoc_part
from common.general import window_over


def parse_data(raw_data):
    """Parse the input"""
    data = raw_data
    return data


def valid_password_a(pwd):
    """Return true if valid"""
    s = str(pwd)
    pair = False
    inc = True
    for p in window_over(s, 2):
        if p[0] == p[1]:
            pair = True
        if p[1] < p[0]:
            inc = False
    return pair and inc


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    cnt = 0
    for pwd in range(*data):
        if valid_password_a(pwd):
            cnt += 1

    return cnt


def valid_password_b(pwd):
    """Return true if valid"""
    s = str(pwd)
    pair = False
    inc = True
    for p in window_over(s, 2):
        if p[1] < p[0]:
            inc = False

    track = [(s[0], 1)]
    for p in s[1:]:
        if p == track[-1][0]:
            track[-1] = (p, track[-1][1] + 1)
            continue
        track.append((p, 1))

    pair = False
    for _, r in track:
        if r == 2:
            pair = True
            break

    return pair and inc


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    cnt = 0
    for pwd in range(*data):
        if valid_password_b(pwd):
            cnt += 1

    return cnt


MY_DATA = (183564, 657475)

solve_part_a(MY_DATA)
solve_part_b(MY_DATA)
