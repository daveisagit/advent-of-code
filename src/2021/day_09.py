"""Advent of code 2021
--- Day 9: Smoke Basin ---
"""

from collections import deque
import math
from operator import add
from common.aoc import file_to_list, aoc_part, get_filename
from common.grid_2d import RC, directions


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        row = [int(c) for c in line]
        data.append(row)
    return data


def get_lows(data, as_position=False):
    """Return a list of the low values (or low positions)"""
    lows = []
    for rn, row in enumerate(data):
        for cn, h in enumerate(row):
            surround = []
            if rn > 0:
                surround.append(data[rn - 1][cn])
            if rn < len(data) - 1:
                surround.append(data[rn + 1][cn])
            if cn > 0:
                surround.append(data[rn][cn - 1])
            if cn < len(row) - 1:
                surround.append(data[rn][cn + 1])
            if h < min(surround):
                lows.append(RC(rn, cn) if as_position else h)
    return lows


def fill_basin_at(data, low: RC) -> int:
    """Return the size of the basin,
    use a flood fill setting a loc to 10 when flooded"""
    pot = deque()
    pot.append(low)
    cnt = 0
    seen = set()
    while pot:
        pos = pot.popleft()
        if pos in seen:
            continue

        seen.add(pos)
        data[pos.row][pos.col] = 10
        cnt += 1
        for d in directions.values():
            nxt_pos = RC(*tuple(map(add, d, pos)))
            if not 0 <= nxt_pos.row < len(data):
                continue
            if not 0 <= nxt_pos.col < len(data[0]):
                continue
            nxt_val = data[nxt_pos.row][nxt_pos.col]
            if nxt_val >= 9:
                continue
            pot.append(nxt_pos)

    return cnt


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    lows = get_lows(data)
    return len(lows) + sum(lows)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    lows = get_lows(data, as_position=True)
    basins = sorted([fill_basin_at(data, low) for low in lows], reverse=True)
    return math.prod(basins[:3])


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
