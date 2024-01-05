"""Advent of code 2021
--- Day 11: Dumbo Octopus ---
"""

from collections import deque
from operator import add
from common.aoc import file_to_list, aoc_part, get_filename
from common.grid_2d import RC, all_directions


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        row = [int(c) for c in line]
        data.append(row)
    return data


def dump_grid(data):
    """Nice visual"""

    def fmt(v):
        v = str(v)
        if v == "0":
            return "\033[1;37;40m0\033[0;0m"
        return v

    print()
    for row in data:
        print("".join(fmt(v) for v in row))


def iterate(data):
    """Iterate 1 step as per instructions"""

    flashes = deque()
    done = set()

    data_plus_1 = []
    for row in data:
        data_plus_1.append([v + 1 for v in row])

    for ri, row in enumerate(data_plus_1):
        for ci, v in enumerate(row):
            if v == 10:
                flashes.append(RC(ri, ci))

    while flashes:
        flash = flashes.pop()
        if flash in done:
            continue
        done.add(flash)

        for d in all_directions:
            nxt_pos = RC(*tuple(map(add, d, flash)))
            if not 0 <= nxt_pos.row < len(data_plus_1):
                continue
            if not 0 <= nxt_pos.col < len(data_plus_1[0]):
                continue
            nxt_val = data_plus_1[nxt_pos.row][nxt_pos.col]
            nxt_val += 1
            data_plus_1[nxt_pos.row][nxt_pos.col] = nxt_val
            if nxt_val >= 10:
                flashes.append(nxt_pos)

    nxt_data = []
    for row in data_plus_1:
        nxt_data.append([v if v < 10 else 0 for v in row])
    return nxt_data, len(done)


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    total_flashes = 0
    for _ in range(100):
        data, flashes = iterate(data)
        total_flashes += flashes
    return total_flashes


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    grid_size = len(data) * len(data[0])
    for step in range(99999):  # some nonsense limit
        data, flashes = iterate(data)
        if flashes == grid_size:
            break

    return step + 1


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
