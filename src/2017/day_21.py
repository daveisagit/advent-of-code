"""Advent of code 2017
--- Day 21: Fractal Art ---
"""

from collections import Counter
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok
from common.grid_2d import dihedral_arrangements, draw_grid, window_join, window_split


def parse_data(raw_data):
    """Parse the input"""
    maps = {}
    for line in raw_data:
        arr = tok(line, "=>")
        maps[arr[0]] = arr[1]
    return maps


def grid_2_pattern(grid):
    """Convert to pattern"""
    rows = ["".join(r) for r in grid]
    return "/".join(rows)


def pattern_2_grid(pattern):
    """Convert to grid"""
    arr = tok(pattern, "/")
    grid = []
    for row in arr:
        row = list(row)
        grid.append(row)
    return grid


def create_maps(data, sz):
    """Create all the maps for a given size"""
    l = sz * sz + sz - 1
    maps = {a: b for a, b in data.items() if len(a) == l}
    all_maps = {}
    for a, b in maps.items():
        a = pattern_2_grid(a)
        for _, _, d in dihedral_arrangements(a):
            d = grid_2_pattern(d)
            if d not in all_maps:
                all_maps[d] = b
    return all_maps


def iterate_old(grid, maps):
    """Perform a mapping, return new layout"""
    rows = len(grid)
    cols = len(grid[0])
    sz = 3
    if rows % 2 == 0:
        sz = 2
    nsz = sz + 1

    new_grid = []

    # row_idx and col_idx are the top left of each window
    # iterate over each window using them as the local origin
    for row_idx in range(0, rows - sz + 1, sz):

        # start with an empty row slice (a row of windows)
        # for the new output size
        new_row_slice = []
        for _ in range(nsz):
            new_row_slice.append([])

        for col_idx in range(0, cols - sz + 1, sz):

            # get the current row of windows
            row_slice = grid[row_idx : row_idx + sz]

            # build the window
            window = []
            for row in row_slice:
                window.append(row[col_idx : col_idx + sz])

            # map to the new window
            window = grid_2_pattern(window)
            window = maps[window]
            window = pattern_2_grid(window)

            # extend the new row of windows
            for i in range(nsz):
                new_row_slice[i].extend(window[i])

        # extend the new grid
        new_grid.extend(new_row_slice)

    return new_grid


def iterate(grid, maps):
    """Perform a mapping, return new layout"""
    rows = len(grid)
    sz = 3
    if rows % 2 == 0:
        sz = 2

    windows = window_split(grid, (sz, sz))

    new_windows = []
    for wr in windows:
        new_wr = []
        for window in wr:
            # map to the new window
            window = grid_2_pattern(window)
            window = maps[window]
            window = pattern_2_grid(window)
            # add to the new row of windows
            new_wr.append(window)
        new_windows.append(new_wr)

    return window_join(new_windows)


def iterate_n(data, n=5) -> int:
    """n iterations"""
    m2 = create_maps(data, 2)
    m3 = create_maps(data, 3)
    maps = {**m2, **m3}
    grid = pattern_2_grid(".#./..#/###")
    for _ in range(n):
        grid = iterate(grid, maps)
    return grid


@aoc_part
def solve_part_a(data, iterations=5) -> int:
    """Solve part A"""
    grid = iterate_n(data, iterations)
    p = grid_2_pattern(grid)
    cnt = Counter(p)
    return cnt["#"]


@aoc_part
def solve_part_b(data, iterations=18) -> int:
    """Solve part B"""
    grid = iterate_n(data, iterations)
    p = grid_2_pattern(grid)
    cnt = Counter(p)
    return cnt["#"]


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA, iterations=2)
solve_part_a(MY_DATA)

solve_part_b(MY_DATA)
