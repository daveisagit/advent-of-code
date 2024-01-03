"""Advent of code 2021
--- Day 7: The Treachery of Whales ---
"""

from common.aoc import file_to_string, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    data = tok(raw_data, delim=",")
    data = [int(n) for n in data]
    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    min_p = min(data)
    max_p = max(data)
    fuel = []
    for p in range(min_p, max_p + 1):
        f = sum(abs(d - p) for d in data)
        fuel.append(f)
    return min(fuel)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    min_p = min(data)
    max_p = max(data)
    fuel = []
    for p in range(min_p, max_p + 1):
        fs = 0
        for crab in data:
            n = abs(crab - p)
            f = (n + 1) * n // 2
            fs += f
        fuel.append(fs)
    return min(fuel)


EX_RAW_DATA = file_to_string(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
