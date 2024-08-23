"""Advent of code 2023
--- Day 13: Point of Incidence ---
"""

from copy import deepcopy
from common.aoc import file_to_list, aoc_part, get_filename
from common.grid_2d import transpose


def parse_data(raw_data):
    """Parse the input - return a 2D list"""
    grid = []
    layouts = []
    for line in raw_data:
        if line:
            grid.append(list(line))
            continue
        layouts.append(grid)
        grid = []
    layouts.append(grid)
    return layouts


def find_vertical_reflections(grid):
    """Return a list of all the possible vertical lines of reflection"""
    w = len(grid[0])
    reflections = []
    for rl in range(1, w):
        rw = min(rl, w - rl)
        if all(line[rl - rw : rl] == line[rl : rl + rw][::-1] for line in grid):
            reflections.append(rl)
    return reflections


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    total = 0
    for grid in data:
        v_lines = find_vertical_reflections(grid)
        t_grid = transpose(grid)
        h_lines = find_vertical_reflections(t_grid)
        assert len(v_lines) + len(h_lines) == 1
        if h_lines:
            total += 100 * h_lines[0]
        else:
            total += v_lines[0]
    return total


def find_smudge(grid):
    """Return the new summary value once we've found a cell
    makes a different reflection line"""
    v_lines = set(find_vertical_reflections(grid))
    t_grid = transpose(grid)
    h_lines = set(find_vertical_reflections(t_grid))
    for r in range(0, len(grid)):
        for c in range(0, len(grid[0])):
            s_grid = deepcopy(grid)
            if s_grid[r][c] == "#":
                s_grid[r][c] = "."
            else:
                s_grid[r][c] = "#"

            # get a second set of possible reflection lines
            v_lines_2 = set(find_vertical_reflections(s_grid))
            t_grid_2 = transpose(s_grid)
            h_lines_2 = set(find_vertical_reflections(t_grid_2))

            # look for a positive change
            if len(v_lines_2) >= len(v_lines) and v_lines_2 != v_lines:
                assert len(v_lines_2 - v_lines) == 1
                return list(v_lines_2 - v_lines)[0]
            if len(h_lines_2) >= len(h_lines) and h_lines_2 != h_lines:
                assert len(h_lines_2 - h_lines) == 1
                return list(h_lines_2 - h_lines)[0] * 100


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    total = 0
    for grid in data:
        total += find_smudge(grid)
    return total


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
