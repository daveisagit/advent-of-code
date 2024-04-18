"""Advent of code 2015
--- Day 15: Science for Hungry People ---
"""

from collections import defaultdict
from math import prod
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok
from common.partitions import compositions


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        arr = tok(line, ":")
        ing = arr[0]
        arr = tok(arr[1], ",")
        prs = {}
        for p in arr:
            pv = tok(p)
            prs[pv[0]] = int(pv[1])
        data.append((ing, prs))

    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    best = 0
    for cmp in compositions(100, len(data)):
        prop_sums = defaultdict(int)
        for i, amt in enumerate(cmp):
            for p, score in data[i][1].items():
                if p == "calories":
                    continue
                prop_sums[p] += amt * score
        prop_sums = {p: s if s > 0 else 0 for p, s in prop_sums.items()}
        overall_score = prod(prop_sums.values())
        best = max(best, overall_score)

    return best


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    best = 0
    for cmp in compositions(100, len(data)):
        prop_sums = defaultdict(int)
        cal_count = 0
        for i, amt in enumerate(cmp):
            for p, score in data[i][1].items():
                if p == "calories":
                    cal_count += score * amt
                    continue
                prop_sums[p] += amt * score
        if cal_count == 500:
            prop_sums = {p: s if s > 0 else 0 for p, s in prop_sums.items()}
            overall_score = prod(prop_sums.values())
            best = max(best, overall_score)

    return best


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)


MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
