"""Advent of code 2018
--- Day 1: Chronal Calibration ---
"""

from common.aoc import file_to_list, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        data.append(int(line))
    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    print(data)
    return sum(data)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    freq = {0}
    s = 0
    while True:
        for i in data:
            s += i
            if s in freq:
                return s
            freq.add(s)


MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(MY_DATA)
solve_part_b(MY_DATA)
