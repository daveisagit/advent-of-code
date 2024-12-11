"""Advent of code 2024
--- Day 11: Plutonian Pebbles ---
"""

from collections import Counter

from common.aoc import (
    aoc_part,
    get_filename,
    file_to_string,
)
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    arr = tok(raw_data)
    data = tuple(int(x) for x in arr)
    return data


def iterate(stones):
    ns = []
    for s in stones:
        if s == 0:
            ns.append(1)
            continue
        ss = str(s)
        if len(ss) % 2 == 0:
            ns.append(int(ss[: len(ss) // 2]))
            ns.append(int(ss[len(ss) // 2 :]))
            continue
        ns.append(s * 2024)
    return tuple(ns)


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    for _ in range(25):
        data = iterate(data)
    return len(data)


def new_stones(v):
    ns = []
    if v == 0:
        ns.append(1)
    elif len(str(v)) % 2 == 0:
        ss = str(v)
        ns.append(int(ss[: len(ss) // 2]))
        ns.append(int(ss[len(ss) // 2 :]))
    else:
        ns.append(v * 2024)
    return Counter(ns)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    current = Counter(data)

    for _ in range(75):
        next = Counter()
        for d, c in current.items():
            ns = new_stones(d)
            for k in ns.keys():
                ns[k] = ns[k] * c
            next.update(ns)
        current = next

    return sum(current.values())


EX_RAW_DATA = file_to_string(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
