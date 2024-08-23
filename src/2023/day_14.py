"""Advent of code 2023
--- Day 14: Parabolic Reflector Dish ---
"""

from bisect import bisect
from common.aoc import file_to_list, aoc_part, get_filename
from common.grid_2d import grid_lists_to_dict


def parse_data(raw_data):
    """Parse the input"""
    size = len(raw_data)
    dish = grid_lists_to_dict(raw_data, content_filter="#O")
    return size, dish


def dump(size, dish):
    """Visual"""
    for r in range(size):
        row = ""
        for c in range(size):
            row += dish.get((r, c), ".")
        print(row)


def tilt(size, dish):
    """Return state after tilting"""
    new_dish = {}

    # for each column
    for c in range(size):

        block_rows = sorted([p[0] for p, t in dish.items() if t == "#" and p[1] == c])
        rock_rows = sorted([p[0] for p, t in dish.items() if t == "O" and p[1] == c])
        new_rock_rows = []

        for r in rock_rows:
            last_rock = max(new_rock_rows, default=-1)
            block_idx = bisect(block_rows, r)
            if block_idx == 0:
                new_rock_row = last_rock + 1
            else:
                new_rock_row = max(block_rows[block_idx - 1], last_rock) + 1
            new_rock_rows.append(new_rock_row)

        for b in block_rows:
            new_dish[(b, c)] = "#"

        for r in new_rock_rows:
            new_dish[(r, c)] = "O"

    return new_dish


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    size, dish = data
    dish = tilt(size, dish)
    return sum((size - p[0]) for p, t in dish.items() if t == "O")


def turn_right(size, dish):
    """We tilt NWSE, which is the same as turning right and tilting up"""
    new_dish = {}
    for p, t in dish.items():
        np = (p[1], size - p[0] - 1)
        new_dish[np] = t
    return new_dish


def cycle(size, dish):
    """Return the state after a cycle of tilts"""
    for _ in range(4):
        dish = tilt(size, dish)
        dish = turn_right(size, dish)
    return dish


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    size, dish = data
    states = {}
    loads = []
    cycles = 0
    repeat_from = None
    while True:
        # cycle 0 is the start state
        load = sum((size - p[0]) for p, t in dish.items() if t == "O")
        loads.append(load)
        state = frozenset(p for p, t in dish.items() if t == "O")
        if state in states:
            repeat_from = states[state]
            repeat_to = cycles
            break
        states[state] = cycles

        dish = cycle(size, dish)
        cycles += 1

    m = repeat_to - repeat_from
    print(f"Repeats between cycle {repeat_from} and {repeat_to}")
    gc = ((1000000000 - repeat_from) % m) + repeat_from
    return loads[gc]


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
