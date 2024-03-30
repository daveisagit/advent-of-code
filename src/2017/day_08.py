"""Advent of code 2017
--- Day 8: I Heard You Like Registers ---
"""

import re
from common.aoc import file_to_list, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    instructions = []
    registers = set()
    for line in raw_data:
        result = re.search(r"(.+) (dec|inc) (-?\d+) if (.+) (.+) (-?\d+)", line)
        ra = result.group(1)
        oa = result.group(2)
        amt = int(result.group(3))
        rb = result.group(4)
        ob = result.group(5)
        cmp = int(result.group(6))
        instructions.append((ra, oa, amt, rb, ob, cmp))
        registers.add(ra)
        registers.add(rb)
    return registers, instructions


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    registers, instructions = data
    registers = {r: 0 for r in registers}
    for ra, oa, amt, rb, ob, cmp in instructions:
        cond = f"{rb} {ob} {cmp}"
        if eval(cond, None, {rb: registers[rb]}):
            if oa == "dec":
                amt = -amt
            registers[ra] += amt
    return max(registers.values())


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    registers, instructions = data
    registers = {r: 0 for r in registers}
    highest = 0
    for ra, oa, amt, rb, ob, cmp in instructions:
        cond = f"{rb} {ob} {cmp}"
        if eval(cond, None, {rb: registers[rb]}):
            if oa == "dec":
                amt = -amt
            registers[ra] += amt
        highest = max(highest, max(registers.values()))
    return highest


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
