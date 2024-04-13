"""Advent of code 2016
--- Day 20: Firewall Rules ---
"""

from itertools import pairwise
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        r = tuple(int(x) for x in tok(line, "-"))
        r = (r[0], r[1] + 1)
        data.append(r)
    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    lowest = 0
    tests = set(data)
    next_tests = set()
    while tests:
        prv_lowest = lowest
        for a, b in tests:
            if lowest < a:
                next_tests.add((a, b))
            if a <= lowest < b:
                lowest = b
        if prv_lowest == lowest:
            break
        tests = next_tests
    return lowest


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    markers = {2**32}
    for a, b in data:
        markers.add(a)
        markers.add(b)

    markers = sorted(markers)
    total = 0
    for x, y in pairwise(markers):
        exclude = False
        for a, b in data:
            if y < a or x > b:
                continue
            if a <= x and y <= b:
                exclude = True
                break
        if not exclude:
            allowed = y - x
            total += allowed

    return total


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(MY_DATA)
