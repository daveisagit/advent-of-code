"""Advent of code 2023
--- Day 5: If You Give A Seed A Fertilizer ---
"""

from bisect import bisect_left
from itertools import combinations
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok, window_over


def parse_data(raw_data):
    """Parse the input"""
    # return the seeds and
    # store the map ranges as a python range (upper bound excluded)
    # along with the adjustment required
    seeds = tuple(int(x) for x in tok(raw_data[0][6:]) if x)
    maps = []
    ranges = []
    for row in raw_data[2:]:
        if "map" in row:
            continue
        if not row:
            maps.append(tuple(ranges))
            ranges = []
            continue
        arr = [int(x) for x in tok(row)]
        range_map = arr[1], arr[1] + arr[2], arr[0] - arr[1]
        ranges.append(range_map)

    maps.append(tuple(ranges))
    maps = tuple(maps)

    # assert there are no overlapping range maps
    for m in maps:
        for a, b in combinations(m, 2):
            assert not b[0] <= a[0] < b[1]
            assert not b[0] < a[1] <= b[1]
            assert not a[0] <= b[0] < a[1]
            assert not a[0] < b[1] <= a[1]

    return seeds, maps


def normalize_ranges(ranges) -> set:
    """Given a set of ranges normalize them removing overlaps for a
    disjointed result set"""
    markers = []
    for a, b in ranges:
        markers.append(a)
        markers.append(b)
    markers = sorted(markers)
    marked_ranges = [
        (bisect_left(markers, a), bisect_left(markers, b)) for a, b in ranges
    ]

    place_holder = None
    normalized_markers = []
    for i in range(len(markers)):
        if any(ma <= i < mb for ma, mb in marked_ranges):
            if place_holder is None:
                place_holder = i
        else:
            if place_holder is not None:
                normalized_markers.append((place_holder, i))
                place_holder = None

    return {(markers[a], markers[b]) for a, b in normalized_markers}


def range_intersection(x, y):
    """Return the range covering the intersection of x,y (or None)"""
    # max start -> min end
    max_start = max(x[0], y[0])
    min_end = min(x[1], y[1])
    if max_start < min_end:
        return (max_start, min_end)
    return None


def map_ranges(mappings, ranges):
    """Map to the next set of ranges"""
    # mappings are disjoint
    # we ensure disjoint ranges using normalize_ranges
    ranges = normalize_ranges(ranges)
    resulting_ranges = set()
    for a, b, adj in mappings:
        m = (a, b)

        remaining_ranges = set()
        for r in ranges:
            i = range_intersection(r, m)
            if i:
                rr = tuple(x + adj for x in i)
                resulting_ranges.add(rr)
                if i[0] > r[0]:
                    rr = (r[0], i[0])
                    remaining_ranges.add(rr)
                if i[1] < r[1]:
                    rr = (i[1], r[1])
                    remaining_ranges.add(rr)
            else:
                remaining_ranges.add(r)

        # what remains from this mapping is processed by
        # the next mapping
        ranges = remaining_ranges

    # anything still remaining is left as is
    return resulting_ranges | remaining_ranges


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    seeds, mappings = data
    # individual seeds are just ranges of size 1
    # Part A built for Part B :-)
    ranges = [(s, s + 1) for s in seeds]
    for mapping in mappings:
        ranges = map_ranges(mapping, ranges)
    return min(r[0] for r in ranges)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    seeds, mappings = data
    ranges = [(a, a + b) for a, b in window_over(seeds, 2, 2)]
    for mapping in mappings:
        ranges = map_ranges(mapping, ranges)
    return min(r[0] for r in ranges)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
