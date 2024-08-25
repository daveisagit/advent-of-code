"""Advent of code 2023
--- Day 18: Lavaduct Lagoon ---
"""

from itertools import pairwise
from operator import add
import re
from common.aoc import file_to_list, aoc_part, get_filename
from common.grid_2d import directions_UDLR, manhattan, shoelace_area


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        rx = re.search(r"(.) (\d+) \(#(.+)\)", line)
        row = rx.group(1), int(rx.group(2)), rx.group(3)
        data.append(row)
    return data


def get_trench(data):
    """Return the corners of the trench"""
    trench = [(0, 0)]
    for d, amt, hex in data:
        dv = directions_UDLR[d]
        dv = (x * amt for x in dv)
        p = tuple(map(add, trench[-1], dv))
        trench.append(p)
    return trench


def get_fill(data):
    """Return the total excavation

    The area covered by (0,0) (0,2) (2,2) (2,0) is 4 on a continuos

    ###     ···     Area = 2x2
    # #     ·#·     ⌜⌝    ▢▢
    ###     ···     ⌞⌟    ▢▢

    The perimeter is 4 x 2 = 8

    We can determine the internal dots using picks theorem
    A = i + B/2 - 1
    where
    A = Area,
    B = Dots on the Boundary (perimeter)

    i = A - p/2 + 1 = 4-4+1 = 1

    """
    trench = get_trench(data)
    a = shoelace_area(trench)
    p = sum(manhattan(a, b) for a, b in pairwise(trench))
    internal = a + 1 - p // 2  # pick's theorem
    return internal + p


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    return get_fill(data)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    # 0 means R, 1 means D, 2 means L, and 3 means U
    directions = "RDLU"
    new_data = []
    for d, amt, hex in data:
        amt = int(hex[:5], 16)
        d = directions[int(hex[5])]
        new_data.append((d, amt, hex))
    return get_fill(new_data)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
