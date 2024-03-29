"""Advent of code 2018
--- Day 25: Four-Dimensional Adventure ---
"""

from operator import sub
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        arr = tok(line, ",")
        data.append(tuple(int(x) for x in arr))
    return data


def manhattan(a, b=(0, 0, 0, 0)):
    """Returns manhattan distance between a and b"""
    d = tuple(map(sub, a, b))
    return sum(abs(o) for o in d)


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    constellations = []
    for p in data:
        found_in = set()
        for ci, c in enumerate(constellations):
            for q in c:
                if manhattan(p, q) <= 3:
                    found_in.add(ci)
                    break

        if len(found_in) == 0:
            constellations.append({p})
            continue

        if len(found_in) == 1:
            constellations[list(found_in)[0]].add(p)
            continue

        nc = {p}
        for ci in found_in:
            nc = nc | constellations[ci]
        constellations = [
            c for ci, c in enumerate(constellations) if ci not in found_in
        ]
        constellations.append(nc)

    return len(constellations)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    return len(data)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)
