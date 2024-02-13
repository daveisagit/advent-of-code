"""Advent of code 2019
--- Day 12: The N-Body Problem ---
"""

from collections import defaultdict
from itertools import combinations
from math import lcm
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        arr = tok(line[1:-1], ",")
        pos = tuple(int(tok(o, "=")[1]) for o in arr)
        vel = (0, 0, 0)
        data.append((pos, vel))
    return data


def iterate(data):
    """Iterate"""
    cur_pos = [list(m[0]) for m in data]
    cur_vel = [list(m[1]) for m in data]
    for ma, mb in combinations(range(4), 2):
        ma_p = data[ma][0]
        mb_p = data[mb][0]
        for d in range(3):
            if ma_p[d] > mb_p[d]:
                cur_vel[ma][d] -= 1
                cur_vel[mb][d] += 1
            if ma_p[d] < mb_p[d]:
                cur_vel[ma][d] += 1
                cur_vel[mb][d] -= 1

    new_moons = []
    for m in range(4):
        for d in range(3):
            cur_pos[m][d] += cur_vel[m][d]
        nm = (tuple(cur_pos[m]), tuple(cur_vel[m]))
        new_moons.append(nm)

    return new_moons


def calc_energy(moon):
    """Energy calc"""
    pot = sum(abs(v) for v in moon[0])
    kin = sum(abs(v) for v in moon[1])
    return pot * kin


@aoc_part
def solve_part_a(data, steps=100) -> int:
    """Solve part A"""
    moons = data
    for _ in range(steps):
        moons = iterate(moons)
    return sum(calc_energy(m) for m in moons)


def get_dimension_cycles(data):
    """Return the period for each dimension"""
    moons = data
    cnt = 0
    periods = [None] * 3
    prv_states = [defaultdict(int)] * 3
    while not all(periods):
        for d in range(3):
            if periods[d]:
                continue
            # state = (pos,vel) for a given dimension
            state = tuple((moons[m][0][d], moons[m][1][d]) for m in range(4))
            if state in prv_states[d]:
                periods[d] = cnt - prv_states[d][state]
                continue
            prv_states[d][state] = cnt

        moons = iterate(moons)
        cnt += 1
    return periods


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    dc = get_dimension_cycles(data)
    return lcm(*dc)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA, steps=1000)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
