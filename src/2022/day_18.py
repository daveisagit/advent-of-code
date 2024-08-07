"""Advent of code 2022
--- Day 18: Boiling Boulders ---
"""

from itertools import product
from operator import add
import sys
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok

sys.setrecursionlimit(5000)


def get_orthogonal_directions():
    directions = []
    for d in range(3):
        v = [0, 0, 0]
        v[d] = -1
        directions.append(tuple(v))
        v[d] = 1
        directions.append(tuple(v))
    return tuple(directions)


def parse_data(raw_data):
    """Parse the input"""
    data = set()
    for line in raw_data:
        block = tuple(int(x) for x in tok(line, ","))
        data.add(block)
    return data


def get_external_surface_area(data):
    directions = get_orthogonal_directions()
    adjacent_count = 0
    for block in data:
        for d in directions:
            n = tuple(map(add, block, d))
            if n in data:
                adjacent_count += 1

    return len(data) * 6 - adjacent_count


def grid_limits(data):
    limits = []
    for d in range(3):
        limits.append(
            (
                min(block[d] for block in data),
                max(block[d] for block in data),
            )
        )
    return tuple(limits)


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    return get_external_surface_area(data)


def create_solid(data):
    """Return the blocks and the insides as a solid"""

    # similar to a flood fill (remove excess from a surrounding cuboid)
    def chew_away(p):
        if p in cuboid and p not in data:
            cuboid.remove(p)
            for d in directions:
                n = tuple(map(add, p, d))
                chew_away(n)

    directions = get_orthogonal_directions()
    limits = grid_limits(data)
    ranges = [range(d[0] - 1, d[1] + 1) for d in limits]
    cuboid = set(product(*ranges))
    start = tuple([d[0] - 1 for d in limits])

    chew_away(start)

    return cuboid


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    solid = create_solid(data)
    inside = solid - data
    total_surface_area = get_external_surface_area(data)
    inside_surface_area = get_external_surface_area(inside)
    return total_surface_area - inside_surface_area


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
