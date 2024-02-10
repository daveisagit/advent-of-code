"""Advent of code 2019
--- Day 10: Monitoring Station ---
"""

from collections import defaultdict
from math import atan, degrees, gcd, inf, pi
from operator import sub
from common.aoc import file_to_list, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    a = set()
    for ri, row in enumerate(raw_data):
        for ci, c in enumerate(row):
            if c == "#":
                a.add((ri, ci))
    return a


def lines_of_sight(data, o):
    """Return a dictionary keyed on reduced fraction"""
    los = defaultdict(set)
    for a in data:
        if a == o:
            continue
        oa = tuple(map(sub, a, o))
        cd = gcd(*oa)
        oa = tuple(x // cd for x in oa)
        los[oa].add(a)

    # sort the asteroids on a line
    sorted_los = {}
    for l, soa in los.items():
        sorted_los[l] = sorted(soa, key=lambda x: abs(x[0]))

    return sorted_los


def get_monitoring_station(data):
    """Return position and count of visible asteroids"""
    best = 0
    pos = None
    for a in data:
        los = lines_of_sight(data, a)
        cnt = len(los)
        if cnt > best:
            best = cnt
            pos = a
    return pos, best


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    _, best = get_monitoring_station(data)
    return best


def get_angles(los):
    """Return the angles clockwise of each line of sight
    y = rows
    x = cols
                     a
                     ^
                    |
                    -y
                    |
    ms ---- +x ---->

    opp = x
    adj = -y
    """

    angles = {}
    for v in los:

        # get the base angle
        rd, cd = v
        y = -rd
        x = cd
        if y == 0:
            a = inf
        else:
            a = abs(x / y)
        a = atan(a)

        # account for quadrant
        if x >= 0:
            if y >= 0:
                pass
            else:
                a = pi - a
        else:
            if y >= 0:
                a = 2 * pi - a
            else:
                a = pi + a

        angles[v] = degrees(a)
    return angles


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    ms, _ = get_monitoring_station(data)
    los = lines_of_sight(data, ms)
    angles = get_angles(los)
    cw_angles = sorted(angles.items(), key=lambda x: x[1])

    removed = 0
    while True:
        for a in cw_angles:
            closest = los[a[0]].pop(0)
            removed += 1
            if removed == 200:
                return closest[1] * 100 + closest[0]


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
