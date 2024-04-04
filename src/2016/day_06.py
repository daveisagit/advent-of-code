"""Advent of code 2016
--- Day 6: Signals and Noise ---
"""

from collections import Counter
from common.aoc import file_to_list, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    data = raw_data
    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    sz = len(data[0])
    word = ""
    for i in range(sz):
        col = [c[i] for c in data]
        cnt = Counter(col)
        c = cnt.most_common()[0][0]
        word += c
    return word


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    sz = len(data[0])
    word = ""
    for i in range(sz):
        col = [c[i] for c in data]
        cnt = Counter(col)
        c = cnt.most_common()[-1][0]
        word += c
    return word


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)


MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)


solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
