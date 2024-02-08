"""Advent of code 2020
--- Day 25: Combo Breaker ---
"""

from common.aoc import file_to_list, aoc_part, get_filename
from common.numty import mod_exp


def parse_data(raw_data):
    """Parse the input"""
    return tuple(int(line) for line in raw_data)


MOD = 20201227


def find_loop_size(pk):
    """Keep multiplying by 7"""
    ls = 0
    while pk != 1:
        pk = (pk * 7) % MOD
        ls += 1
    return MOD - ls - 1


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    card_pk, door_pk = data

    card_ls = find_loop_size(card_pk)
    door_ls = find_loop_size(door_pk)

    card_ek = mod_exp(door_pk, card_ls, MOD)
    door_ek = mod_exp(card_pk, door_ls, MOD)

    if card_ek != door_ek:
        return None

    return door_ek


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
