"""Advent of code 2016
--- Day 2: Bathroom Security ---
"""

from operator import add
from common.aoc import file_to_list, aoc_part, get_filename
from common.grid_2d import directions_UDLR


def parse_data(raw_data):
    """Parse the input"""
    data = raw_data
    return data


chg_map = {"U": -3, "D": 3, "R": 1, "L": -1}


def next_button(v, seq):
    """Return the next button"""
    for d in seq:
        a = chg_map[d]
        if d == "L" and v in (1, 4, 7):
            continue
        if d == "R" and v in (3, 6, 9):
            continue
        if d == "U" and v in (1, 2, 3):
            continue
        if d == "D" and v in (7, 8, 9):
            continue
        if 1 <= v + a <= 9:
            v += a
    return v


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    v = 5
    s = ""
    for line in data:
        v = next_button(v, line)
        s += str(v)

    return s


PAD = """
  1  
 234 
56789
 ABC 
  D  
"""


def next_button_b(p, seq, pad):
    """Return the next button position"""
    for d in seq:
        d = directions_UDLR[d]
        np = tuple(map(add, p, d))
        if np in pad:
            p = np
    return p


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    pad = {}
    for r, ln in enumerate(PAD.splitlines()[1:]):
        for c, ch in enumerate(ln):
            if ch != " ":
                pad[(r, c)] = ch

    p = (2, 0)
    s = ""
    for seq in data:
        p = next_button_b(p, seq, pad)
        s += pad[p]

    return s


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
