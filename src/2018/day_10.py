"""Advent of code 2018
--- Day 10: The Stars Align ---
"""

from operator import add
import re
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok
from common.grid_2d import get_grid_limits, all_directions


def parse_data(raw_data):
    """Parse the input"""

    def get_vector(s):
        arr = tok(s, ",")
        return int(arr[0]), int(arr[1])

    data = []
    for line in raw_data:
        result = re.search(r"position=<(.+)> velocity=<(.+)>", line)
        p = get_vector(result.group(1))
        v = get_vector(result.group(2))
        data.append((p, v))
    return data


def get_grid(data, t=0):
    """See the start at time = t"""
    return [tuple(map(add, p, (v[0] * t, v[1] * t))) for p, v in data]


def dump_grid(grid):
    """See the start at time = t"""
    min_x, min_y, max_x, max_y = get_grid_limits(grid)
    for y in range(min_y, max_y + 1):
        row = ""
        for x in range(min_x, max_x + 1):
            if (x, y) in grid:
                row += "#"
                continue
            row += "."
        print(row)


def stars_aligned(g):
    """Return True if so: every point has a neighbour"""
    g = set(g)
    for p in g:
        cnt = 0
        for d in all_directions:
            np = tuple(map(add, p, d))
            if np in g:
                cnt += 1
        if cnt == 0:
            return False
    return True


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    t = 0
    while True:
        g = get_grid(data, t=t)
        if stars_aligned(g):
            dump_grid(g)
            break
        t += 1

    return t


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
