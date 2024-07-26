"""Advent of code 2022
--- Day 13: Distress Signal ---
"""

from common.aoc import file_to_list, aoc_part, get_filename
from common.general import window_over
from functools import cmp_to_key


def parse_data(raw_data):
    """Parse the input"""
    pairs = []
    for pair in window_over(raw_data, 2, 3):
        pair = [eval(packet) for packet in pair]
        pairs.append(pair)
    return pairs


def compare_ordering(a, b):
    """Return as would fit a compare function
    -1: a<b
     0: a=b
    +1: a>b
    """
    if isinstance(a, int) and isinstance(b, int):
        if a == b:
            return 0
        if a < b:
            return -1
        if a > b:
            return 1
    if isinstance(a, int):
        a = [a]
    if isinstance(b, int):
        b = [b]

    if len(a) == 0 and len(b) == 0:
        return 0
    if len(a) == 0:
        return -1
    if len(b) == 0:
        return 1

    o = compare_ordering(a[0], b[0])
    if o != 0:
        return o
    return compare_ordering(a[1:], b[1:])


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    s = 0
    for idx, pair in enumerate(data):
        if compare_ordering(pair[0], pair[1]) == -1:
            s += idx + 1
    return s


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    packets = [pair[0] for pair in data]
    packets.extend([pair[1] for pair in data])
    packets.append([[2]])
    packets.append([[6]])
    packets = sorted(packets, key=cmp_to_key(compare_ordering))
    a = packets.index([[2]])
    b = packets.index([[6]])
    return (a + 1) * (b + 1)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
