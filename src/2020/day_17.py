"""Advent of code 2020
--- Day 17: Conway Cubes ---
"""

from operator import add
from common.aoc import file_to_list, aoc_part, get_filename
from common.grid_3d import XYZ


def parse_data(raw_data):
    """Parse the input"""
    data = set()
    for y, line in enumerate(raw_data):
        for x, c in enumerate(line):
            if c == "#":
                data.add(XYZ(x, y, 0))
    return data


def limits(data):
    """Limits"""
    min_x = min(c.x for c in data)
    max_x = max(c.x for c in data)
    min_y = min(c.y for c in data)
    max_y = max(c.y for c in data)
    min_z = min(c.z for c in data)
    max_z = max(c.z for c in data)
    return min_x, max_x, min_y, max_y, min_z, max_z


def iterate(data):
    """ "Iterate"""

    def active_neighbors(p):
        an = set()
        for xd in range(-1, 2):
            for yd in range(-1, 2):
                for zd in range(-1, 2):
                    d = (xd, yd, zd)
                    if xd == yd == zd == 0:
                        continue
                    np = XYZ(*tuple(map(add, p, d)))
                    if np in data:
                        an.add(np)
        return an

    new_data = set()
    min_x, max_x, min_y, max_y, min_z, max_z = limits(data)
    for x in range(min_x - 1, max_x + 2):
        for y in range(min_y - 1, max_y + 2):
            for z in range(min_z - 1, max_z + 2):
                p = XYZ(x, y, z)
                an = len(active_neighbors(p))
                if p in data:
                    if 2 <= an <= 3:
                        new_data.add(p)
                    continue
                if an == 3:
                    new_data.add(p)

    return new_data


def limits_4d(data):
    """Limits"""
    min_x = min(c[0] for c in data)
    max_x = max(c[0] for c in data)
    min_y = min(c[1] for c in data)
    max_y = max(c[1] for c in data)
    min_z = min(c[2] for c in data)
    max_z = max(c[2] for c in data)
    min_w = min(c[3] for c in data)
    max_w = max(c[3] for c in data)
    return min_x, max_x, min_y, max_y, min_z, max_z, min_w, max_w


def iterate_4d(data):
    """ "Iterate"""

    def active_neighbors(p):
        an = set()
        for xd in range(-1, 2):
            for yd in range(-1, 2):
                for zd in range(-1, 2):
                    for wd in range(-1, 2):
                        d = (xd, yd, zd, wd)
                        if xd == yd == zd == wd == 0:
                            continue
                        np = tuple(map(add, p, d))
                        if np in data:
                            an.add(np)
        return an

    new_data = set()
    min_x, max_x, min_y, max_y, min_z, max_z, min_w, max_w = limits_4d(data)
    for x in range(min_x - 1, max_x + 2):
        for y in range(min_y - 1, max_y + 2):
            for z in range(min_z - 1, max_z + 2):
                for w in range(min_w - 1, max_w + 2):
                    p = (x, y, z, w)
                    an = len(active_neighbors(p))
                    if p in data:
                        if 2 <= an <= 3:
                            new_data.add(p)
                        continue
                    if an == 3:
                        new_data.add(p)

    return new_data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    for _ in range(6):
        data = iterate(data)
    return len(data)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    data = {(x, y, z, 0) for x, y, z in data}
    for _ in range(6):
        data = iterate_4d(data)
    return len(data)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
