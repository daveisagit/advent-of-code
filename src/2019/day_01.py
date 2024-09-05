"""Advent of code 2019
--- Day 1: The Tyranny of the Rocket Equation ---
"""

from common.aoc import file_to_list, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    data = [int(line) for line in raw_data]
    return data


def fuel_required(mass):
    """How much!"""
    f = mass // 3
    f -= 2
    return f


def fuel_required_b(mass):
    """How much!"""
    tf = 0
    f = mass
    while True:
        f = fuel_required(f)
        if f <= 0:
            return tf
        tf += f


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    return sum(fuel_required(m) for m in data)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    return sum(fuel_required_b(m) for m in data)


MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(MY_DATA)

solve_part_b(MY_DATA)
