"""Advent of code 2022
--- Day 9: Rope Bridge ---
"""

from operator import add, sub
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import sign, tok
from common.grid_2d import directions_UDLR


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        arr = tok(line)
        step = arr[0], int(arr[1])
        data.append(step)
    return data


def adjust_tail(h, t) -> tuple:
    dif = tuple(map(sub, h, t))
    dif = (sign(x) for x in dif)
    if abs(h[0] - t[0]) > 1 or abs(h[1] - t[1]) > 1:
        return tuple(map(add, t, dif))
    return t


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    h = (0, 0)
    t = (0, 0)
    tail_visits = {t}
    for dn, amt in data:
        d = directions_UDLR[dn]
        for _ in range(amt):
            h = tuple(map(add, h, d))
            t = adjust_tail(h, t)
            tail_visits.add(t)

    return len(tail_visits)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    rope = [(0, 0)] * 10
    tail_visits = {(0, 0)}
    for dn, amt in data:
        d = directions_UDLR[dn]
        for _ in range(amt):
            rope[0] = tuple(map(add, rope[0], d))  # move the head
            for idx in range(1, 10):
                rope[idx] = adjust_tail(rope[idx - 1], rope[idx])
            tail_visits.add(rope[-1])

    return len(tail_visits)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
