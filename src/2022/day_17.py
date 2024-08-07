"""Advent of code 2022
--- Day 17: Pyroclastic Flow ---
"""

from operator import add
from common.aoc import file_to_string, aoc_part, get_filename

rock_types = (
    ((0, 2), (0, 3), (0, 4), (0, 5)),
    ((0, 3), (1, 2), (1, 3), (1, 4), (2, 3)),
    ((0, 2), (0, 3), (0, 4), (1, 4), (2, 4)),
    ((0, 2), (1, 2), (2, 2), (3, 2)),
    ((0, 2), (0, 3), (1, 2), (1, 3)),
)


def parse_data(raw_data):
    """Parse the input"""
    data = raw_data
    return data


def run_for_n_rocks(n_rocks, data, cave=None, jet_pointer=0):
    """Run the simulation for n rock falls, return the jet pointer"""
    jet_length = len(data)
    if cave is None:
        cave = set()

    for rc in range(n_rocks):

        highest_rock = max([p[0] for p in cave], default=0)

        rock_type = rock_types[rc % len(rock_types)]
        rock = tuple(tuple(map(add, p, (highest_rock + 4, 0))) for p in rock_type)
        while True:

            # Can we move sideways?
            jet_char = data[jet_pointer]
            jet = 1
            if jet_char == "<":
                jet = -1

            jet_pointer += 1
            jet_pointer %= jet_length

            rock_move = tuple(tuple(map(add, p, (0, jet))) for p in rock)
            if all(0 <= p[1] < 7 for p in rock_move) and all(
                p not in cave for p in rock_move
            ):
                rock = rock_move

            # have we hit rock or bottom
            nxt_rock = tuple(tuple(map(add, p, (-1, 0))) for p in rock)
            if any(p in cave for p in nxt_rock) or any(p[0] == 0 for p in nxt_rock):
                for p in rock:
                    cave.add(p)
                break

            rock = nxt_rock

        # prune the cave, find highest rock in each column
        # cut off from the lowest of them
        base = min(
            max([p[0] for p in cave if p[1] == col], default=0) for col in range(7)
        )
        for p in list(cave):
            if p[0] < base:
                cave.remove(p)

    return jet_pointer


def print_cave(cave):
    """Visualise the cave"""
    height = max(p[0] for p in cave)
    base = min(p[0] for p in cave)
    print(f"Highest: {height}")
    for h in range(height, base - 1, -1):
        s = "|"
        for x in range(7):
            c = "."
            if (h, x) in cave:
                c = "#"
            s += c
        s += "|"
        print(s)


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    cave = set()
    run_for_n_rocks(2022, data, cave=cave)
    return max([p[0] for p in cave], default=0)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    n_rocks = 1000000000000
    m = len(rock_types)
    cave = set()
    states = {}
    jc = 0
    rock_count = 0
    # look for a repeated state (jet pointer, cave layout)
    # to get a rock modulus and height difference
    while True:
        jc = run_for_n_rocks(m, data, cave=cave, jet_pointer=jc)
        rock_count += m
        height = max([p[0] for p in cave], default=0)

        fc = frozenset((p[0] - height, p[1]) for p in cave)
        if (jc, fc) in states:
            rock_modulus = rock_count - states[(jc, fc)][0]
            height_diff = height - states[(jc, fc)][1]
            break
        states[(jc, fc)] = rock_count, height

    rounds = n_rocks // rock_modulus
    remainder = n_rocks % rock_modulus

    # find the extra height from the remainder by running once more
    cave = set()
    run_for_n_rocks(remainder, data, cave=cave)
    extra_height = max([p[0] for p in cave], default=0)

    return rounds * height_diff + extra_height


EX_RAW_DATA = file_to_string(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
