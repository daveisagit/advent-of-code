"""Advent of code 2024
--- Day 14: Restroom Redoubt ---
"""

import re

from collections import Counter
from math import prod
from operator import add

from common.aoc import (
    file_to_list,
    aoc_part,
    get_filename,
)
from common.general import sign
from common.grid_2d import (
    print_single_char_dict_grid,
    all_directions,
)


def parse_data(raw_data):
    """Parse the input"""
    # p=0,4 v=3,-3
    ps = []
    vs = []
    for line in raw_data:
        sr = re.search(r"p=(-?\d+),(-?\d+)\sv=(-?\d+),(-?\d+)", line)
        d = tuple(int(g) for g in sr.groups())
        p = d[:2]
        v = d[2:]
        ps.append(tuple(p))
        vs.append(tuple(v))

    return ps, vs


def iterate(ps, vs, sz):
    new_ps = []
    for p, v in zip(ps, vs):
        p = tuple(map(add, p, v))
        p = tuple(x % s for x, s in zip(p, sz))
        new_ps.append(p)
    return new_ps


@aoc_part
def solve_part_a(data, sz=(11, 7)) -> int:
    """Solve part A"""
    # sz=(cols-x,rows-y)
    ps, vs = data
    qs = []
    for _ in range(100):
        ps = iterate(ps, vs, sz)

    # create quads (-1,-1) (-1,1) (1,-1) (1,1)
    for p in ps:
        q = tuple(sign(x - s // 2) for x, s in zip(p, sz))
        # ignore on the divide
        if q[0] == 0 or q[1] == 0:
            continue
        qs.append(q)

    qc = Counter(qs)
    return prod(qc.values())


@aoc_part
def solve_part_b(data, sz=(101, 103)) -> int:
    """Solve part B"""

    def aligned(s, limit):
        """Consider as aligned if the number of isolated bots < limit"""
        s = set(s)
        c = 0
        for p in s:
            has_neighbour = False
            for d in all_directions:
                np = tuple(map(add, p, d))
                if np in s:
                    has_neighbour = True
                    break
            if has_neighbour:
                continue
            c += 1
            if c > limit:
                return False
        return True

    ps, vs = data

    # define what it means to be aligned
    pct = 70
    limit = len(ps) - (len(ps) * pct) // 100

    cnt = 0
    while True:

        # iterate
        ps = iterate(ps, vs, sz)
        cnt += 1
        if cnt % 1000 == 0:
            print(cnt)

        # check alignment
        if aligned(ps, limit):
            tps = [(y, x) for x, y in ps]
            grid = Counter(tps)
            print_single_char_dict_grid(grid, none_char=".")
            return cnt


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA, sz=(101, 103))

solve_part_b(MY_DATA)
