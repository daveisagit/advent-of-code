"""Advent of code 2021
--- Day 25: Sea Cucumber ---
"""

from common.aoc import file_to_list, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input, return rows, cols, east, south"""
    east = set()
    south = set()
    for ri, line in enumerate(raw_data):
        for ci, c in enumerate(line):
            if c == ">":
                east.add((ri, ci))
            if c == "v":
                south.add((ri, ci))
    return len(raw_data), len(raw_data[0]), east, south, True


def dump_grid(data):
    """Visual"""
    rows, cols, east, south, changed = data
    print(changed)
    for row in range(rows):
        line = ["."] * cols
        for sc in [c for r, c in east if r == row]:
            line[sc] = ">"
        for sc in [c for r, c in south if r == row]:
            line[sc] = "v"
        line = "".join(line)
        print(line)


def iterate(data):
    """next"""
    changed = False
    rows, cols, east, south, _ = data
    new_east = set()
    for r, c in east:
        nr = r
        nc = c
        nc += 1
        nc %= cols
        if (nr, nc) in east or (nr, nc) in south:
            new_east.add((r, c))
        else:
            new_east.add((nr, nc))
            changed = True
    east = new_east

    new_south = set()
    for r, c in south:
        nr = r
        nc = c
        nr += 1
        nr %= rows
        if (nr, nc) in east or (nr, nc) in south:
            new_south.add((r, c))
        else:
            new_south.add((nr, nc))
            changed = True
    south = new_south

    return rows, cols, east, south, changed


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    cnt = 0
    while True:
        cnt += 1
        data = iterate(data)
        changed = data[4]
        if not changed:
            break

    return cnt


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)
