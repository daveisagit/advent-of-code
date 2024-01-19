"""Advent of code 2020
--- Day 9: Encoding Error ---
"""

from itertools import combinations
from common.aoc import file_to_list, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    data = [int(v) for v in raw_data]
    return data


def first_invalid(data, preamble_size=5):
    """Return the first invalid number"""
    for idx, v in enumerate(data):
        if idx < preamble_size:
            continue
        preamble = data[idx - preamble_size : idx]
        valid_values = [a + b for a, b in combinations(preamble, 2)]
        if v not in valid_values:
            return v
    return None


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    if len(data) == 20:
        return first_invalid(data)
    return first_invalid(data, preamble_size=25)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    sz = len(data)
    if sz == 20:
        fi = first_invalid(data)
    else:
        fi = first_invalid(data, preamble_size=25)

    for l in range(3, sz):
        for idx in range(0, sz - l):
            ss = data[idx : idx + l]
            if len(ss) != l:
                raise ValueError("Grr")
            if sum(ss) == fi:
                ss = sorted(ss)
                return ss[0] + ss[-1]

    return len(data)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
