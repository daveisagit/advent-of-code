"""Advent of code 2020
--- Day 11: Seating System ---
"""

from operator import add
from common.aoc import file_to_list, aoc_part, get_filename
from common.grid_2d import all_directions


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        data.append(list(line))
    return data


def dump_grid(g):
    """visual"""
    for row in g:
        line = "".join(row)
        print(line)


def iterate(g, occ_lim=4, los=False):
    """return a new grid"""
    rows = len(g)
    cols = len(g[0])
    state_changed = False

    def occupied_surrounds(ir, ic):
        cp = (ir, ic)
        s = set()
        rng = 1
        if los:
            rng = max(rows, cols)

        if ir == 0 and ic == 6:
            pass

        for d in all_directions:
            for r in range(1, rng + 1):
                md = tuple(v * r for v in d)
                np = tuple(map(add, cp, md))
                if not (0 <= np[0] < rows and 0 <= np[1] < cols):
                    break
                nc = g[np[0]][np[1]]
                if nc == "#":
                    s.add(np)
                    break
                if nc == "L":
                    break
        return s

    ng = []
    for ir, row in enumerate(g):
        nr = []
        for ic, spot in enumerate(row):
            if spot == ".":
                nr.append(".")
                continue
            if spot == "L":
                if not occupied_surrounds(ir, ic):
                    nr.append("#")
                    state_changed = True
                    continue
            if spot == "#":
                if len(occupied_surrounds(ir, ic)) >= occ_lim:
                    nr.append("L")
                    state_changed = True
                    continue
            nr.append(spot)
        ng.append(nr)
    return ng, state_changed


def seat_count(g, cc="#"):
    """Return seat count"""
    return len([c for row in g for c in row if c == cc])


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    grid = data
    cnt = 0
    while True:
        cnt += 1
        grid, changed = iterate(grid)
        if not changed:
            break

    return seat_count(grid)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    grid = data
    cnt = 0
    while True:
        cnt += 1
        grid, changed = iterate(grid, occ_lim=5, los=True)
        if not changed:
            break

    return seat_count(grid)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
