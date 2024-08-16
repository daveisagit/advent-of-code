"""Advent of code 2023
--- Day 4: Scratchcards ---
"""

import re
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    lines = []
    for line in raw_data:
        rr = re.search(r".+:(.+)\|(.+)", line)
        card = frozenset(int(x) for x in tok(rr.group(1)) if x)
        numbers = frozenset(int(x) for x in tok(rr.group(2)) if x)
        lines.append((card, numbers))
    return lines


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    total = 0
    for card, numbers in data:
        matches = len(card & numbers)
        if matches:
            val = 2 ** (matches - 1)
            total += val
    return total


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    copies = [1] * len(data)
    for cn, (card, numbers) in enumerate(data):
        matches = len(card & numbers)
        # we get x more copies of the next few
        # where x is the number of copies of this card
        for i in range(cn + 1, cn + 1 + matches):
            copies[i] += copies[cn]
    return sum(copies)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
