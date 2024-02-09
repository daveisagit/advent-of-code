"""Advent of code 2019
--- Day 3: Crossed Wires ---
"""

from operator import add
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok
from common.grid_2d import directions_UDLR, manhattan


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        steps = tok(line, ",")
        steps = [(step[0], int(step[1:])) for step in steps]
        data.append(steps)
    return data


def get_trace(wire):
    """Trace the wires locations"""
    trace = {}
    cur = (0, 0)
    dst = 0
    for d, amt in wire:
        d = directions_UDLR[d]
        for _ in range(amt):
            dst += 1
            cur = tuple(map(add, cur, d))
            trace[cur] = dst
    return trace


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    trace_a = set(get_trace(data[0]))
    trace_b = set(get_trace(data[1]))
    overlaps = trace_a.intersection(trace_b)
    res = min(manhattan(o) for o in overlaps)
    return res


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    trace_a = get_trace(data[0])
    trace_b = get_trace(data[1])
    set_a = set(trace_a)
    set_b = set(trace_b)
    overlaps = set_a.intersection(set_b)
    res = min(trace_a[o] + trace_b[o] for o in overlaps)

    return res


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
