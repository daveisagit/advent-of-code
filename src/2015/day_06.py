"""Advent of code 2015
--- Day 6: Probably a Fire Hazard ---
"""

from collections import defaultdict
import re
from common.aoc import file_to_list, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        rr = re.search(
            r"(turn off|turn on|toggle) (\d+),(\d+) through (\d+),(\d+)", line
        )
        op = rr.group(1)
        vals = [int(v) for v in rr.groups()[1:]]
        a = (vals[0], vals[1])
        b = (vals[2] + 1, vals[3] + 1)
        data.append((op, a, b))
    return data


def get_markers(data):
    """Hows the grid divided in terms of blocks"""
    markers = []
    for dim in range(2):
        vals_1 = {x[1][dim] for x in data}
        vals_2 = {x[2][dim] for x in data}
        vals = vals_1 | vals_2
        vals.update({0, 1000})
        vals = sorted(vals)
        markers.append(vals)
    return markers


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    markers = get_markers(data)
    state = defaultdict(bool)
    for op, (ax, ay), (bx, by) in data:

        axi = markers[0].index(ax)
        bxi = markers[0].index(bx)
        ayi = markers[1].index(ay)
        byi = markers[1].index(by)

        for xi in range(axi, bxi):
            for yi in range(ayi, byi):
                blk = (xi, yi)
                if op == "turn on":
                    state[blk] = True
                if op == "turn off":
                    state[blk] = False
                if op == "toggle":
                    state[blk] = not state[blk]

    total = 0
    for (xi, yi), ft in state.items():
        if not ft:
            continue
        x_amt = markers[0][xi + 1] - markers[0][xi]
        y_amt = markers[1][yi + 1] - markers[1][yi]
        total += x_amt * y_amt

    return total


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    markers = get_markers(data)
    state = defaultdict(int)
    for op, (ax, ay), (bx, by) in data:

        axi = markers[0].index(ax)
        bxi = markers[0].index(bx)
        ayi = markers[1].index(ay)
        byi = markers[1].index(by)

        for xi in range(axi, bxi):
            for yi in range(ayi, byi):
                blk = (xi, yi)
                if op == "turn on":
                    state[blk] += 1
                if op == "turn off":
                    if state[blk] > 0:
                        state[blk] -= 1
                if op == "toggle":
                    state[blk] += 2

    total = 0
    for (xi, yi), b in state.items():
        x_amt = markers[0][xi + 1] - markers[0][xi]
        y_amt = markers[1][yi + 1] - markers[1][yi]
        total += b * x_amt * y_amt

    return total


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(MY_DATA)
