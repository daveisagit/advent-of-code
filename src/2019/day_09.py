"""Advent of code 2019
--- Day 9: Sensor Boost ---
"""

from common.aoc import aoc_part, file_to_string, get_filename
from common.intcode import IntCode


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    ic = IntCode(data)
    outputs = ic.run([1])
    return outputs


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    ic = IntCode(data)
    outputs = ic.run([2])
    return outputs


MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))

solve_part_a(MY_RAW_DATA)
solve_part_b(MY_RAW_DATA)
