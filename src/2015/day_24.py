"""Advent of code 2015
--- Day 24: It Hangs in the Balance ---
"""

from heapq import heappop, heappush
from itertools import combinations
from math import prod
from common.aoc import file_to_list, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    data = [int(x) for x in raw_data]
    return data


def get_qe3(data):
    """Get QE for 3 groups"""
    target = sum(data) // 3
    data = sorted(data)
    rt = 0
    for i, v in enumerate(data):
        rt += v
        if rt >= target:
            break
    max_nbr = i

    data = sorted(data, reverse=True)
    rt = 0
    for i, v in enumerate(data):
        rt += v
        if rt >= target:
            break
    min_nbr = i + 1

    ways = set()
    for i in range(min_nbr, max_nbr + 1):
        for cmb in combinations(data, i):
            if sum(cmb) == target:
                way = frozenset(cmb)
                ways.add(way)

    ways = sorted(ways, key=lambda x: (len(x), prod(x)))

    for a in ways:
        for b in ways:
            if a & b:
                continue
            return prod(a)

    return None


def get_qe4(data):
    """Get QE for 4 groups"""
    target = sum(data) // 4
    data = sorted(data)
    rt = 0
    for i, v in enumerate(data):
        rt += v
        if rt >= target:
            break
    max_nbr = i

    data = sorted(data, reverse=True)
    rt = 0
    for i, v in enumerate(data):
        rt += v
        if rt >= target:
            break
    min_nbr = i + 1

    ways = set()
    for i in range(min_nbr, max_nbr + 1):
        for cmb in combinations(data, i):
            if sum(cmb) == target:
                way = frozenset(cmb)
                ways.add(way)

    ways = sorted(ways, key=lambda x: (len(x), prod(x)))

    for a in ways:
        for b in ways:
            if a & b:
                continue

            for c in ways:
                if a & c or b & c:
                    continue
                return prod(a)

    return None


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    return get_qe3(data)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    return get_qe4(data)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
