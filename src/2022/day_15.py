"""Advent of code 2022
--- Day 15: Beacon Exclusion Zone ---
"""

from itertools import pairwise, product
import re
from common.aoc import file_to_list, aoc_part, get_filename
from common.grid_2d import manhattan


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        rr = re.search(
            r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)",
            line,
        )
        values = [int(g) for g in rr.groups()]
        sensor = values[0], values[1]
        beacon = values[2], values[3]
        pair = sensor, beacon
        data.append(pair)
    return data


@aoc_part
def solve_part_a(data, y=10) -> int:
    """Solve part A"""
    regions = []
    beacons_on_row = set()

    # find the regions of row=y that are covered by scanners
    # note any beacons on row=y
    for sensor, beacon in data:
        if beacon[1] == y:
            beacons_on_row.add(beacon[0])
        md = manhattan(sensor, beacon)
        if sensor[1] - md <= y <= sensor[1] + md:
            width = md - abs(sensor[1] - y)
            a = sensor[0] - width
            b = sensor[0] + width + 1
            regions.append((a, b))

    # build a sorted list of markers for where regions start/end
    markers = [r[0] for r in regions]
    markers.extend([r[1] for r in regions])
    markers = sorted(set(markers))

    coverage = 0
    for a, b in pairwise(markers):
        for ra, rb in regions:
            if ra <= a < rb:
                coverage += b - a
                break

    return coverage - len(beacons_on_row)


def to_alt(p):
    return p[0] + p[1], p[0] - p[1]


def from_alt(p):
    return (p[0] + p[1]) // 2, (p[0] - p[1]) // 2


@aoc_part
def solve_part_b(data, lim=20) -> int:
    """Solve part B"""
    # create square regions in the alternate grid (twisted 45)
    regions = []
    for sensor, beacon in data:
        md = manhattan(sensor, beacon)
        alt_sensor = to_alt(sensor)
        corner_a = alt_sensor[0] - md, alt_sensor[1] - md
        corner_b = alt_sensor[0] + md + 1, alt_sensor[1] + md + 1
        region = corner_a, corner_b
        regions.append(region)

    # create the marker sets for each dimension
    # including the limits of the search
    # excluding markers outside them
    alt_lim = 2 * lim + 1
    markers_0 = {0, alt_lim}
    markers_0.update(r[0][0] for r in regions if 0 <= r[0][0] < alt_lim)
    markers_0.update(r[1][0] for r in regions if 0 <= r[1][0] < alt_lim)
    markers_0 = sorted(markers_0)

    alt_lim_lower = -2 * lim
    alt_lim_upper = 2 * lim + 1
    markers_1 = {alt_lim_lower, alt_lim_upper}
    markers_1.update(
        r[0][1] for r in regions if alt_lim_lower <= r[0][1] < alt_lim_upper
    )
    markers_1.update(
        r[1][1] for r in regions if alt_lim_lower <= r[1][1] < alt_lim_upper
    )
    markers_1 = sorted(markers_1)

    # create a set of all possible regions
    markers = set((a, b) for a, b in product(markers_0, markers_1))

    # remove those covered by sensor coverage
    for m_0 in markers_0:
        for m_1 in markers_1:
            for a, b in regions:
                if a[0] <= m_0 < b[0] and a[1] <= m_1 < b[1]:
                    markers.discard((m_0, m_1))

    # remove those outside the limits
    candidates = set()
    for m in markers:
        m = from_alt(m)
        if 0 <= m[0] <= lim and 0 <= m[1] <= lim:
            candidates.add(m)

    if len(candidates) > 1:
        raise RuntimeError("Should only be 1")

    beacon = list(candidates)[0]

    return beacon[0] * 4000000 + beacon[1]


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA, y=2000000)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA, lim=4000000)
