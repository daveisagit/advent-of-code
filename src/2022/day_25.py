"""Advent of code 2022
--- Day 25: Full of Hot Air ---
"""

from common.aoc import file_to_list, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    return raw_data


sym = "=-012"


def snafu_2_dec(s):
    t = 0
    for p, ch in enumerate(s[::-1]):
        pv = 5**p
        cf = sym.index(ch) - 2
        t += pv * cf
    return t


def dec_2_snafu(dec):
    res = ""
    while dec > 0:
        rem = dec % 5
        rem += 2
        dec = dec // 5
        if rem >= 5:
            dec += 1
        rem %= 5
        dig = sym[rem]
        res = dig + res
    return res


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    return dec_2_snafu(sum(snafu_2_dec(s) for s in data))


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    return len(data)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)
