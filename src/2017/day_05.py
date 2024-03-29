"""Advent of code 2017
--- Day 5: A Maze of Twisty Trampolines, All Alike ---
"""

from common.aoc import file_to_list, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    return tuple(int(x) for x in raw_data)


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    jumps = list(data)
    idx = 0
    steps = 0
    while True:
        try:
            prv_idx = idx
            idx = idx + jumps[idx]
            jumps[prv_idx] += 1
            steps += 1
        except IndexError:
            return steps


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    jumps = list(data)
    idx = 0
    steps = 0
    while True:
        try:
            prv_idx = idx
            idx = idx + jumps[idx]
            if jumps[prv_idx] < 3:
                jumps[prv_idx] += 1
            else:
                jumps[prv_idx] -= 1
            steps += 1
        except IndexError:
            return steps


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
