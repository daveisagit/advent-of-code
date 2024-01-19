"""Advent of code 2020
--- Day 10: Adapter Array ---
"""

from collections import Counter
from itertools import pairwise
from common.aoc import file_to_list, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    data = [int(v) for v in raw_data]
    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    data.append(0)
    data.append(max(data) + 3)
    data = sorted(data)
    jolts = [b - a for a, b in pairwise(data)]
    cnt = Counter(jolts)
    return cnt[1] * cnt[3]


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    data = sorted(data)
    end = max(data)
    memo = {}

    def combos(jolt) -> int:
        if jolt in memo:
            return memo[jolt]
        if jolt == end:
            total = 1
        else:
            options = [j for j in data if jolt < j <= jolt + 3]
            total = 0
            for o in options:
                total += combos(o)
        memo[jolt] = total
        return total

    return combos(0)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
