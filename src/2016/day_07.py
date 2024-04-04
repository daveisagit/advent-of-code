"""Advent of code 2016
--- Day 7: Internet Protocol Version 7 ---
"""

import re
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import window_over


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        d = re.split(r"\[|\]", line)
        data.append(d)
    return data


def contains_abba(s):
    """Return True if so"""
    for w in window_over(s, 4, 1):
        if w[0] == w[3] and w[1] == w[2] and w[0] != w[1]:
            return True
    return False


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    c = 0
    for ip in data:
        if not any(contains_abba(p) for p in ip[::2]):
            continue
        if len(ip) > 1:
            if any(contains_abba(p) for p in ip[1::2]):
                continue
        c += 1
    return c


def contains_aba(s):
    """Return True if so"""
    oc = set()
    for w in window_over(s, 3, 1):
        if w[0] == w[2] and w[0] != w[1]:
            oc.add((w[0], w[1]))
    return oc


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    c = 0
    for ip in data:

        abas = set()
        babs = set()
        for p in ip[::2]:
            abas.update(contains_aba(p))

        if len(ip) > 1:
            for p in ip[1::2]:
                babs.update(contains_aba(p))

        for aba in abas:
            bab = (aba[1], aba[0])
            if bab in babs:
                c += 1
                break

    return c


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
