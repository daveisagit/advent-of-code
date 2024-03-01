"""Advent of code 2018
--- Day 5: Alchemical Reduction ---
"""

from common.aoc import file_to_string, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    data = raw_data
    return data


alpha_lower = list(map(chr, range(ord("a"), ord("z") + 1)))
alpha_upper = list(map(chr, range(ord("A"), ord("Z") + 1)))
units_1 = [l + u for l, u in zip(alpha_lower, alpha_upper)]
units_2 = [u + l for l, u in zip(alpha_lower, alpha_upper)]
units = units_1 + units_2


def reduce_polymer(polymer):
    """As per spec"""
    while True:
        cur_length = len(polymer)
        for p in units:
            polymer = polymer.replace(p, "")
        if len(polymer) == cur_length:
            break
    return polymer


@aoc_part
def solve_part_a(data: str) -> int:
    """Solve part A"""
    return len(reduce_polymer(data))


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    shortest = len(data)
    for ir in range(26):
        polymer = data.replace(alpha_lower[ir], "")
        polymer = polymer.replace(alpha_upper[ir], "")
        polymer = reduce_polymer(polymer)
        if len(polymer) < shortest:
            shortest = len(polymer)
    return shortest


EX_RAW_DATA = file_to_string(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
