"""Advent of code 2018
--- Day 3: No Matter How You Slice It ---
"""

from collections import defaultdict
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        arr = tok(line, "@")
        arr = tok(arr[1], ":")
        pos = tok(arr[0], ",")
        siz = tok(arr[1], "x")
        pos = [int(x) for x in pos]
        siz = [int(x) for x in siz]
        patch = ((pos[0], pos[0] + siz[0]), (pos[1], pos[1] + siz[1]))
        data.append(patch)
    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    patches = defaultdict(int)
    for p in data:
        for x in range(p[0][0], p[0][1]):
            for y in range(p[1][0], p[1][1]):
                patches[(x, y)] += 1
    overlaps = [p for p, c in patches.items() if c > 1]
    return len(overlaps)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    patches = defaultdict(int)
    for p in data:
        for x in range(p[0][0], p[0][1]):
            for y in range(p[1][0], p[1][1]):
                patches[(x, y)] += 1
    singles = [p for p, c in patches.items() if c == 1]
    for idx, p in enumerate(data):
        single = True
        for x in range(p[0][0], p[0][1]):
            for y in range(p[1][0], p[1][1]):
                if (x, y) not in singles:
                    single = False
                    break
            if not single:
                break
        if single:
            return idx + 1

    return None


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
