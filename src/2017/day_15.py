"""Advent of code 2017
--- Day 15: Dueling Generators ---
"""

from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    return tuple(int(tok(line)[-1]) for line in raw_data)


BITS_31 = 2**31 - 1
BITS_16 = 2**16 - 1
MLT = (16807, 48271)
A_40M = 40000000
B_5M = 5000000

assert BITS_31 == 2147483647
assert BITS_16 == 65535


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    a, b = data
    ma, mb = MLT
    cnt = 0
    for _ in range(A_40M):
        a = (a * ma) % BITS_31
        b = (b * mb) % BITS_31
        if (a & BITS_16) == (b & BITS_16):
            cnt += 1
    return cnt


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    a, b = data
    ma, mb = MLT
    cnt = 0
    for _ in range(B_5M):
        while True:
            a = (a * ma) % BITS_31
            if a % 4 == 0:
                break

        while True:
            b = (b * mb) % BITS_31
            if b % 8 == 0:
                break

        if (a & BITS_16) == (b & BITS_16):
            cnt += 1
    return cnt


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
