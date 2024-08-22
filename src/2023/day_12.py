"""Advent of code 2023
--- Day 12: Hot Springs ---
"""

from functools import lru_cache
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        arr = tok(line)
        pattern = arr[0]
        damaged = tuple(int(x) for x in tok(arr[1], ","))
        data.append((pattern, damaged))
    return data


@lru_cache(maxsize=None)
def valid_arrangements(pattern, damaged) -> int:
    arrangements = 0
    min_space_required = sum(damaged) + len(damaged) - 1
    for i in range(0, len(pattern) - min_space_required + 1):
        left = pattern[:i]
        window = pattern[i : i + damaged[0]]
        right = pattern[i + damaged[0] :]
        if "#" in left:
            break
        if "." in window:
            continue
        if right and right[0] == "#":
            continue

        if len(damaged) == 1:
            if "#" not in right:
                arrangements += 1
        else:
            arrangements += valid_arrangements(right[1:], damaged[1:])
    return arrangements


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    return sum(valid_arrangements(pattern, damaged) for pattern, damaged in data)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    total = 0
    for pattern, damaged in data:
        pattern = "?".join([pattern] * 5)
        damaged = damaged * 5
        total += valid_arrangements(pattern, damaged)
    return total


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
