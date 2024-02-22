"""Advent of code 2019
--- Day 21: Springdroid Adventure ---
"""

from common.aoc import aoc_part, file_to_string, get_filename
from common.intcode import IntCode


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A
    Always jump if D=1 and if either A,B or C is 0  (i.e. A ^ B ^ C = 0)
    ABCD
    ???1
        @
    #####...#####
    """
    ic = IntCode(data)
    script = [
        "OR A T",
        "AND B T",
        "AND C T",
        "NOT T J",
        "AND D J",
        "WALK",
    ]
    o = ic.run_ascii(script)
    for l in o:
        print(l)
    return None


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B
    So we jump if we need to as per part a when ~(A ^ B ^ C) ^ D over a gap onto a landing spot
    But then after that we must either
    a) Walk to E with I being available if need be
    b) Walk to F (a jump to J is not known, so leave it as that)
    c) jump straight away again to H
    """
    ic = IntCode(data)
    script = [
        # Walk to F: E^F
        "OR E J",
        "AND F J",
        # Walk to E: and jump to I: E^I
        "OR E T",
        "AND I T",
        "OR T J",
        # Jump to H
        "OR H J",
        # clear T for part A
        "NOT J T",
        "AND J T",
        # As part A - if either A,B or C are 0
        "OR A T",
        "AND B T",
        "AND C T",
        "NOT T T",
        # T = ~(A ^ B ^ C) T means there is a gap to jump
        "AND T J",
        "AND D J",
        "RUN",
    ]
    o = ic.run_ascii(script)
    for l in o:
        print(l)
    return None


MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))

solve_part_a(MY_RAW_DATA)
solve_part_b(MY_RAW_DATA)
