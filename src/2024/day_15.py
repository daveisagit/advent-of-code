"""Advent of code 2024
--- Day 15: Warehouse Woes ---
"""

from operator import add

from common.aoc import (
    file_to_list,
    aoc_part,
    get_filename,
)
from common.general import input_sections
from common.grid_2d import directions, print_single_char_dict_grid


def parse_data(raw_data):
    """Parse the input"""
    secs = input_sections(raw_data)
    grid = {}
    bot = None
    for ri, row in enumerate(secs[0]):
        for ci, ch in enumerate(row):
            p = (ri, ci)
            if ch == "@":
                bot = p
                ch = "."
            grid[p] = ch
    moves = []
    for line in secs[1]:
        line = list(line)
        moves.extend(line)
    return grid, bot, moves


def try_box(grid, p, dc):
    d = directions[dc]
    np = tuple(map(add, p, d))
    if grid[np] == "#":
        return False
    if grid[np] == "O":
        if not try_box(grid, np, dc):
            return False
    grid[np] = "O"
    grid[p] = "."
    return True


def attempt_move(grid, p, dc):
    d = directions[dc]
    np = tuple(map(add, p, d))
    if grid[np] == "#":
        return p
    if grid[np] == "O":
        if try_box(grid, np, dc):
            return np
        else:
            return p
    return np


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    grid, bot, moves = data
    p = bot
    for dc in moves:
        p = attempt_move(grid, p, dc)
    gps = 0
    for p, ch in grid.items():
        if ch == "O":
            r, c = p
            gps += 100 * r + c

    return gps


def parse_data_b(raw_data):
    """Parse the input for part B"""
    secs = input_sections(raw_data)
    grid = {}
    bot = None
    for ri, row in enumerate(secs[0]):
        for ci, ch in enumerate(row):
            p = (ri, ci * 2)
            p2 = (ri, ci * 2 + 1)
            ch1 = ch
            ch2 = ch
            if ch == "@":
                bot = p
                ch1 = "."
                ch2 = "."
            if ch == "O":
                ch1 = "["
                ch2 = "]"

            grid[p] = ch1
            grid[p2] = ch2
    moves = []
    for line in secs[1]:
        line = list(line)
        moves.extend(line)
    return grid, bot, moves


def get_box_moves(grid, p, dc):
    """Return the locations to move, called recursively. None means do not move"""
    d = directions[dc]
    np = tuple(map(add, p, d))

    # hit a wall cant move
    if grid[np] == "#":
        return None

    # there is space, we can move p into its desired spot
    if grid[np] == ".":
        return [p]

    # knock on effect for horizontal movement
    if dc in "<>":
        bm = get_box_moves(grid, np, dc)
        if bm is None:
            return None
        else:
            return bm + [p]

    # knock on effect for vertical movement
    bms = []

    # branching into 2 parts
    # np1, np2 set based on which end is being pushed
    if grid[np] == "[":
        np1 = np
        np2 = tuple(map(add, np, (0, 1)))

    if grid[np] == "]":
        np1 = tuple(map(add, np, (0, -1)))
        np2 = np

    # only move if both branches can move
    bm = get_box_moves(grid, np1, dc)
    if bm is None:
        return None
    else:
        bms += bm

    bm = get_box_moves(grid, np2, dc)
    if bm is None:
        return None
    else:
        bms += bm

    return bms + [p]


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    grid, bot, moves = parse_data_b(data)

    p = bot
    for dc in moves:

        # Visualise each iteration
        # grid[p] = "@"
        # print_single_char_dict_grid(grid)
        # grid[p] = "."

        box_moves = get_box_moves(grid, p, dc)
        if box_moves is None:
            continue

        d = directions[dc]
        p = tuple(map(add, p, d))

        seen = set()
        for bp in box_moves:  # do the last first
            # ignore possibility of duplicate move requests
            if bp in seen:
                continue
            seen.add(bp)
            ch = grid[bp]
            np = tuple(map(add, bp, d))
            grid[bp] = "."
            grid[np] = ch

    gps = 0
    for p, ch in grid.items():
        if ch in "[":
            r, c = p
            gps += 100 * r + c

    return gps


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_RAW_DATA)
solve_part_b(MY_RAW_DATA)
