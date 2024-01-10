"""Advent of code 2021
--- Day 19: Beacon Scanner ---
"""

from collections import deque
from operator import add, sub
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok
from common.grid_3d import XYZ, all_90_rotations, rotate_a_point

ALL_ROTATIONS = all_90_rotations()


def parse_data(raw_data):
    """Parse the input"""
    data = []
    scanner = None
    for line in raw_data:
        if not line:
            continue
        if "scanner" in line:
            if scanner:
                data.append(scanner)
            scanner = set()
            continue
        arr = tok(line, delim=",")
        scanner.add(XYZ(*[int(c) for c in arr]))

    data.append(scanner)

    return data


def compare_scanners(beacons_a, beacons_b):
    """Are there any beacons in common"""

    for r in ALL_ROTATIONS:
        beacons_b_r = {rotate_a_point(b, r) for b in beacons_b}  # b'
        # check every possible point pairing between a and b'
        for a in beacons_a:
            for b in beacons_b_r:
                d = tuple(map(sub, a, b))
                test = {tuple(map(add, d, b)) for b in beacons_b_r}
                test.intersection_update(beacons_a)
                if len(test) >= 12:
                    return r, d


def analyse(data):
    """Solve part A"""
    # Do a minimal spanning tree using BFS of the network of scanners
    # starting with scanner 0 (arbitrary)

    bfs = deque()
    bfs.append((0, []))
    seen = set()
    all_beacons = set()
    origins = {}
    while bfs:
        scanner_idx, transforms = bfs.popleft()
        if scanner_idx in seen:
            continue
        seen.add(scanner_idx)
        scanner_a = data[scanner_idx]

        # back track through the transforms so we have the
        # points in the same coordinate system as scanner 0
        beacons = scanner_a
        origin = (0, 0, 0)
        for transform in transforms[::-1]:
            r, d = transform
            # transform the points to the previous coordinate system
            # on the path using the same r,d that discovered the
            # common points with the previous scanner on the path
            beacons = {rotate_a_point(b, r) for b in beacons}  # b'
            beacons = {tuple(map(add, d, b)) for b in beacons}
            origin = rotate_a_point(origin, r)
            origin = tuple(map(add, d, origin))

        all_beacons.update(beacons)
        origins[scanner_idx] = origin

        # expand the network if there are common beacons
        for idx, scanner_b in enumerate(data):
            if idx in seen:
                continue
            res = compare_scanners(scanner_a, scanner_b)
            if res:
                bfs.append((idx, transforms + [res]))

    return all_beacons, origins


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    all_beacons, _ = data
    return len(all_beacons)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    _, origins = data
    lm = 0
    for o1 in origins.values():
        for o2 in origins.values():
            d = tuple(map(sub, o1, o2))
            m = sum(abs(o) for o in d)
            if m > lm:
                lm = m
    return lm


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

analysis_example = analyse(EX_DATA)
analysis_data = analyse(MY_DATA)

solve_part_a(analysis_example)
solve_part_a(analysis_data)

solve_part_b(analysis_example)
solve_part_b(analysis_data)
