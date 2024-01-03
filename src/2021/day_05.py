"""Advent of code 2021
--- Day 5: Hydrothermal Venture ---
"""

from common.aoc import file_to_list, aoc_part, get_filename
from common.general import sign, tok
from common.grid_2d import XY, Line


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        points = tok(line, delim="->")
        coords_a = tok(points[0], ",")
        coords_b = tok(points[1], ",")
        point_a = XY(int(coords_a[0]), int(coords_a[1]))
        point_b = XY(int(coords_b[0]), int(coords_b[1]))
        data.append(Line(point_a, point_b))

    return data


def only_orthogonal(data):
    """Just the V/H lines"""
    vh = []
    for line in data:
        line: Line
        if line.a.x == line.b.x or line.a.y == line.b.y:
            vh.append(line)
    return vh


def only_diagonal(data):
    """Just the diagonal lines"""
    dg = []
    for line in data:
        if abs(line.a.x - line.b.x) == abs(line.a.y - line.b.y):
            dg.append(line)
    return dg


def get_limits(lines):
    """Return the limits of the data"""
    min_x = min(min(line.a.x, line.b.x) for line in lines)
    max_x = max(max(line.a.x, line.b.x) for line in lines)
    min_y = min(min(line.a.y, line.b.y) for line in lines)
    max_y = max(max(line.a.y, line.b.y) for line in lines)
    return min_x, min_y, max_x, max_y


def get_overlap_count(lines) -> int:
    """Find the number of overlapped points from the lines"""
    _, _, max_x, max_y = get_limits(lines)
    grid = []
    for _ in range(max_x + 1):
        line = [0] * (max_y + 1)
        grid.append(line)

    for line in lines:
        line: Line
        xd = sign(line.b.x - line.a.x)
        yd = sign(line.b.y - line.a.y)
        steps = max(abs(line.a.x - line.b.x), abs(line.a.y - line.b.y))
        for i in range(steps + 1):
            grid[line.a.x + i * xd][line.a.y + i * yd] += 1

    grid_count = 0
    for line in grid:
        line_count = sum(1 for p in line if p > 1)
        grid_count += line_count

    return grid_count


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    lines = only_orthogonal(data)
    return get_overlap_count(lines)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    lines = only_orthogonal(data)
    dg = only_diagonal(data)
    lines.extend(dg)
    return get_overlap_count(lines)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
