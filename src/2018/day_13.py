"""Advent of code 2018
--- Day 13: Mine Cart Madness ---
"""

from copy import deepcopy
from operator import add
from common.aoc import aoc_part, file_to_list_no_strip, get_filename
from common.grid_2d import directions


def parse_data(raw_data):
    """Parse the input"""

    carts = []
    track = []
    for r, line in enumerate(raw_data):
        row = list(line)
        track.append(row)
        for c, ch in enumerate(line):
            if ch in directions:
                carts.append((r, c, ch, 1))

    for r, c, ch, _ in carts:
        if ch in "^v":
            track[r][c] = "|"
        else:
            track[r][c] = "-"

    return track, carts


def iterate(track, carts, clear_collision=False):
    """Return new cart positions and crash location"""

    # map for \
    corner_map_1 = {
        "^": "<",
        "<": "^",
        "v": ">",
        ">": "v",
    }

    # map for /
    corner_map_2 = {
        "^": ">",
        "<": "v",
        "v": "<",
        ">": "^",
    }

    collision = None
    collisions = []
    new_carts = []
    positions = set((r, c) for r, c, _, _ in sorted(carts))
    for r, c, dc, turn in sorted(carts):

        if clear_collision:
            if (r, c) in collisions:
                continue

        new_turn = turn
        ndc = dc
        d = directions[dc]
        pos = (r, c)
        positions.remove(pos)
        nr, nc = tuple(map(add, pos, d))

        if (nr, nc) in positions:
            collision = (nr, nc)
            if clear_collision:
                collisions.append(collision)
                continue
            break

        positions.add((nr, nc))

        tk = track[nr][nc]

        if tk == "\\":
            ndc = corner_map_1[dc]

        if tk == "/":
            ndc = corner_map_2[dc]

        if tk == "+":
            di = list(directions).index(dc)
            di += turn
            di %= 4
            ndc = list(directions)[di]
            new_turn = turn - 1
            if new_turn < -1:
                new_turn = 1

        new_carts.append((nr, nc, ndc, new_turn))

    new_carts = [(r, c, d, t) for r, c, d, t in new_carts if (r, c) not in collisions]

    return new_carts, collision


def draw_track(track, carts):
    """Visual"""
    track = deepcopy(track)
    for r, c, ch, _ in carts:
        track[r][c] = ch
    print()
    for row in track:
        print("".join(row))


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    track, carts = data
    while True:
        carts, collision = iterate(track, carts)
        if collision:
            break
    return f"{collision[1]},{collision[0]}"


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    track, carts = data
    while len(carts) > 1:
        carts, _ = iterate(track, carts, clear_collision=True)
    cart = carts[0]
    return f"{cart[1]},{cart[0]}"


EX_RAW_DATA_A = file_to_list_no_strip(get_filename(__file__, "ex"))
EX_DATA_A = parse_data(EX_RAW_DATA_A)

EX_RAW_DATA_B = file_to_list_no_strip(get_filename(__file__, "xb"))
EX_DATA_B = parse_data(EX_RAW_DATA_B)

MY_RAW_DATA = file_to_list_no_strip(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA_A)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA_B)
solve_part_b(MY_DATA)
