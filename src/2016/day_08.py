"""Advent of code 2016
--- Day 8: Two-Factor Authentication ---
"""

import re
from common.aoc import file_to_list, aoc_part, get_filename
from common.grid_2d import transpose


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        if line.startswith("rect"):
            rr = re.search(r"rect (\d+)x(\d+)", line)
            dim = tuple(int(x) for x in rr.groups())
            data.append(("rect", dim))
            continue
        if line.startswith("rotate"):
            rr = re.search(r"rotate (column|row) [x|y]=(\d+) by (\d+)", line)
            data.append(("rotate", rr.group(1), int(rr.group(2)), int(rr.group(3))))

    return data


def create_grid(sz):
    """Create an empty grid"""
    grid = []
    for r in range(sz[0]):
        row = [0] * sz[1]
        grid.append(row)
    return grid


def add_rect(grid, dim):
    """Add rect"""
    for r in range(dim[1]):
        for c in range(dim[0]):
            grid[r][c] = 1


def rotate_row(grid, row_num, amt):
    """Rotate row"""
    new_grid = grid[:row_num]
    row = grid[row_num]
    row = row[-amt:] + row[:-amt]
    new_grid.append(row)
    if row_num < len(grid) - 1:
        new_grid.extend(grid[row_num + 1 :])
    return new_grid


def draw(grid):
    """Visual"""
    for row in grid:
        row = "".join(["#" if x == 1 else "." for x in row])
        print(row)


@aoc_part
def solve_part_a(data, sz=(3, 7)) -> int:
    """Solve part A"""

    g = create_grid(sz)
    for d in data:
        if d[0] == "rect":
            add_rect(g, d[1])
            continue
        if d[0] == "rotate":
            if d[1] == "row":
                g = rotate_row(g, d[2], d[3])
            if d[1] == "column":
                g = transpose(g)
                g = rotate_row(g, d[2], d[3])
                g = transpose(g)

    draw(g)

    return sum(sum(r) for r in g)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    return len(data)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA, sz=(6, 50))
