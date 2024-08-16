"""Advent of code 2022
--- Day 23: Unstable Diffusion ---
"""

from collections import Counter
from operator import add
from common.aoc import file_to_list, aoc_part, get_filename
from common.grid_2d import get_grid_limits, grid_lists_to_dict, all_directions


def parse_data(raw_data):
    """Parse the input"""
    elves = list(grid_lists_to_dict(raw_data, content_filter="#").keys())
    return elves


# NSWE
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def get_proposed_moves(idx: int):
    orth = directions[idx]
    if idx < 2:
        return [(orth[0], c) for c in range(-1, 2)]
    else:
        return [(r, orth[1]) for r in range(-1, 2)]


def get_next(current: list, round_idx: int) -> list:
    current_set = set(current)
    next_list = []
    for p in current:
        np = p
        if any(tuple(map(add, p, d)) in current_set for d in all_directions):

            for i in range(4):
                idx = (round_idx + i) % 4
                moves = get_proposed_moves(idx)
                new_pos = [tuple(map(add, p, m)) for m in moves]
                if not any(p in current_set for p in new_pos):
                    np = tuple(map(add, p, directions[idx]))
                    break

        next_list.append(np)

    summary = Counter(next_list)
    collisions = {p for p, cnt in summary.items() if cnt > 1}
    next_list = [current[i] if p in collisions else p for i, p in enumerate(next_list)]

    return next_list


def print_grid(grid):
    min_x, min_y, max_x, max_y = get_grid_limits(grid)
    print()
    for r in range(min_y, max_y + 1):
        row = ""
        for c in range(min_x, max_x + 1):
            ch = "."
            if (r, c) in grid:
                ch = "#"
            row += ch
        print(row)


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    elves = data
    for r in range(10):
        elves = get_next(elves, r)

    min_x, min_y, max_x, max_y = get_grid_limits(elves)
    rect = (max_x - min_x + 1) * (max_y - min_y + 1)
    return rect - len(elves)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    elves = data
    r = 0
    while True:
        new_elves = get_next(elves, r)
        r += 1
        if new_elves == elves:
            break
        elves = new_elves
    return r


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
