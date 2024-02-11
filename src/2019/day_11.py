"""Advent of code 2019
--- Day 11: Space Police ---
"""

from collections import defaultdict
from operator import add
from common.aoc import aoc_part, file_to_string, get_filename
from common.intcode import IntCode
from common.grid_2d import get_grid_limits, rotations


def paint_hull(data, start_on_white=False) -> defaultdict:
    """Solve part A"""
    ic = IntCode(data)
    tiles = defaultdict(int)
    d = 1  # facing north
    pos = (0, 0)
    if start_on_white:
        tiles[pos] = 1

    while ic.is_running:

        ic.input = [tiles[pos]]
        ic.go()
        if not ic.is_running:
            return tiles

        paint = ic.output[0]
        turn = ic.output[1]
        ic.output.clear()
        tiles[pos] = paint

        # rotate
        if turn == 0:
            # ACW - left
            d += 1
        else:
            # CW - right
            d -= 1
        d %= 4

        # move onto the tile
        pos = tuple(map(add, pos, rotations[d]))

    return None


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    tiles = paint_hull(data)
    if tiles:
        return len(tiles)
    return None


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    tiles = paint_hull(data, start_on_white=True)
    # pick out the white tiles and change to x,y
    tiles = {(t[1], t[0]) for t, c in tiles.items() if c == 1}
    min_x, min_y, max_x, max_y = get_grid_limits(tiles)
    x_width = max_x - min_x + 1
    img = []
    for y in range(min_y, max_y + 1):
        row = [" "] * x_width
        for ix, x in enumerate(range(min_x, max_x + 1)):
            if (x, y) in tiles:
                row[ix] = "#"
        img.append(row)

    for row in img:
        print("".join(row))

    return len(data)


MY_DATA = file_to_string(get_filename(__file__, "my"))

solve_part_a(MY_DATA)
# solve_part_b(MY_DATA)
