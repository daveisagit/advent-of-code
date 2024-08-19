"""Advent of code 2023
--- Day 9: Mirage Maintenance ---
"""

from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok
from common.numty import extend_polynomial_sequence


def parse_data(raw_data):
    """Parse the input"""
    return [[int(x) for x in tok(line)] for line in raw_data]


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    new_seqs = [extend_polynomial_sequence(seq) for seq in data]
    return sum(seq[-1] for seq in new_seqs)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    new_seqs = [extend_polynomial_sequence(seq) for seq in data]
    return sum(seq[0] for seq in new_seqs)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
