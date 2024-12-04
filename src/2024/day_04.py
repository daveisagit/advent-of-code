"""Advent of code 2024
--- Day 4: Ceres Search ---
"""

from common.aoc import (
    file_to_list,
    aoc_part,
    get_filename,
)

from common.grid_2d import (
    dihedral_arrangements,
    window_over_grid,
)


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for r in raw_data:
        data.append(list(r))
    return data


def transpose(grid):
    """Transpose [][]"""
    return list(map(list, zip(*grid)))


def diagonal_1(data):
    """Return the \ diagonals"""
    sz = len(data)
    lines = []
    for d in range(-sz - 1, sz + 1):
        line = []
        for r in range(sz):
            for c in range(sz):
                if r - c == d:
                    line.append(data[r][c])
        lines.append(line)
    return lines


def diagonal_2(data):
    """Return the / diagonals"""
    sz = len(data)
    lines = []
    for d in range(0, sz * 2):
        line = []
        for r in range(sz):
            for c in range(sz):
                if r + c == d:
                    line.append(data[r][c])
        lines.append(line)
    return lines


def xmas_occurrences(line):
    """Return the number XMAS occurrences forward and reverse"""
    s = "".join(line)
    r = s.count("XMAS")
    s = s[::-1]
    r += s.count("XMAS")
    return r


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    s = 0

    lines = diagonal_1(data)
    for l in lines:
        t = xmas_occurrences(l)
        s += t

    lines = diagonal_2(data)
    for l in lines:
        t = xmas_occurrences(l)
        s += t

    for l in data:
        t = xmas_occurrences(l)
        s += t

    data = transpose(data)
    for l in data:
        t = xmas_occurrences(l)
        s += t

    return s


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    # since the X-MAS cross has reflection symmetry we only
    # need to rotate
    # nicer solution would be to rotate the mask and maybe use regex
    cnt = 0
    for _, _, data in dihedral_arrangements(data, just_rotations=True):
        for wdw in window_over_grid(data, (3, 3)):
            if (
                wdw[0][0] == "M"
                and wdw[0][2] == "S"
                and wdw[1][1] == "A"
                and wdw[2][0] == "M"
                and wdw[2][2] == "S"
            ):
                cnt += 1

    return cnt


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
