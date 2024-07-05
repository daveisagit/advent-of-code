"""Advent of code 2022
--- Day 1: Calorie Counting ---
"""

from common.aoc import file_to_list, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    elves = []
    calories = 0
    for row in raw_data:
        if row == "":
            elves.append(calories)
            calories = 0
        else:
            calories = calories + int(row)
    elves.sort(reverse=True)
    return elves


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    return max(data)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    return sum(data[:3])


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)


solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
