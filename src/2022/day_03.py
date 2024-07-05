"""Advent of code 2022
--- Day 3: Rucksack Reorganization ---
"""

from common.aoc import file_to_list, aoc_part, get_filename
from common.general import first, window_over


def get_priority(item: str):
    """the priority of an item
    Lowercase item types a through z have priorities 1 through 26.
    Uppercase item types A through Z have priorities 27 through 52.
    """
    if item.islower():
        return ord(item) - 96
    else:
        return ord(item) - 38


def parse_data(raw_data):
    """Parse the input"""
    return raw_data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    rucksacks = [(line[: len(line) // 2], line[len(line) // 2 :]) for line in data]
    rucksacks = [(set(list(a)), set(list(b))) for a, b in rucksacks]
    return sum(get_priority(first(a & b)) for a, b in rucksacks)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    rucksacks = [set(list(stuff)) for stuff in data]
    total = 0
    for e1, e2, e3 in window_over(rucksacks, 3, 3):
        common_items = e1 & e2 & e3
        total += get_priority(first(common_items))

    return total


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
