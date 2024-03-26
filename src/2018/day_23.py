"""Advent of code 2018
--- Day 23: Experimental Emergency Teleportation ---
"""

from collections import defaultdict
from itertools import combinations, pairwise
from math import inf
from operator import sub
import re
from common.aoc import file_to_list, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        result = re.search(r"pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)", line)
        t = tuple(int(v) for v in result.groups())
        data.append(t)
    return data


def manhattan(a, b=(0, 0, 0)):
    """Returns manhattan distance between a and b"""
    d = tuple(map(sub, a, b))
    return sum(abs(o) for o in d)


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    max_r = max(d[3] for d in data)
    max_nano = [d for d in data if d[3] == max_r][0]
    inside = [d for d in data if manhattan(d[:3], max_nano[:3]) <= max_r]
    return len(inside)


def get_parallel_planes(data):
    """Return the list of nanobots defined by the 4x2
    parallel planes"""
    pp = []
    for nb in data:
        x, y, z, d = nb
        pd = [x + y, x - y, y - x, -x - y]
        pd = [p + z for p in pd]
        pd = [(p - d, p + d) for p in pd]
        pp.append(tuple(pd))
    return pp


def get_intersections(spaces):
    """Return a set of the intersections of all the spaces"""

    def intersect(spa, spb):
        spc = []
        for i in range(4):
            a_from, a_to = spa[i]
            b_from, b_to = spb[i]
            c_from = max(a_from, b_from)
            c_to = min(a_to, b_to)
            d = c_to - c_from
            if d >= 0:
                spc.append((c_from, c_to))
            else:
                spc.append(None)
        return spc

    result = set()
    for cnt, (spa, spb) in enumerate(combinations(spaces, 2)):
        # if cnt % 10000 == 0:
        #     print(cnt, len(result))
        spc = intersect(spa, spb)
        if not all(spc):
            continue
        result.add(tuple(spc))
    return result


def get_range_memberships(spaces):
    """Return membership of indexes to ranges"""

    def for_dimension(dim):
        range_membership_for_dim = defaultdict(set)
        spaces_for_dim = [b[dim] for b in spaces]
        values = sorted(
            list({sp[0] for sp in spaces_for_dim} | {sp[1] for sp in spaces_for_dim})
        )
        for a, b in pairwise(values):
            b -= 1
            for idx, dim_space in enumerate(spaces_for_dim):
                p, q = dim_space
                if max(a, p) <= min(b, q):
                    range_membership_for_dim[(a, b)].add(idx)
        return range_membership_for_dim

    range_membership = []
    for dim in range(4):
        for_dim = for_dimension(dim)
        range_membership.append(for_dim)

    return range_membership


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    # get the octahedrons expressed in an 8=4x2 ordinate format
    # each octahedron is bounded by parallel plane pairs
    # the length of the norm is the manhattan distance
    spaces = get_parallel_planes(data)

    # on each of the 4 dimensions split into linear intervals
    # and find out which nanobots occupy it
    range_memberships = get_range_memberships(spaces)

    # checking the cartesian product for every possible sub-space
    # is too long about 2000^4
    # read the each dimension by popularity, i.e. focus on the central
    # cluster
    rms = []
    for range_membership in range_memberships:
        rm = sorted(range_membership.items(), key=lambda x: len(x[1]), reverse=True)
        rms.append(rm)

    # once we can no longer improve the best intersection quit
    cnt = 0
    most_found = 0
    for i0, (interval_0, indexes_0) in enumerate(rms[0]):
        indexes = indexes_0
        if len(indexes) < most_found:
            break
        for i1, (interval_1, indexes_1) in enumerate(rms[1][: i0 + 1]):
            indexes = indexes & indexes_1
            if len(indexes) < most_found:
                break

            for i2, (interval_2, indexes_2) in enumerate(rms[2][: i1 + 1]):
                indexes = indexes & indexes_2
                if len(indexes) < most_found:
                    break

                for _, (interval_3, indexes_3) in enumerate(rms[3][: i2 + 1]):
                    indexes = indexes & indexes_3
                    cnt += 1
                    if len(indexes) < most_found:
                        break

                    if len(indexes) > most_found:
                        most_found = len(indexes)
                        sweet_spot = interval_0, interval_1, interval_2, interval_3
                        print(
                            f"# bots = {len(indexes)} within all these 4 plane limits {sweet_spot}"
                        )

    # now we know the manhattan values for the 8 planes
    # which is is closest to the origin
    # check all the possible points inside the sweet spot area
    # reverse calc to get limits for x,y,z

    shortest_md = inf
    interval_0, interval_1, interval_2, interval_3 = sweet_spot
    possible_points = set()
    for i0 in range(interval_0[0], interval_0[1]):
        for i1 in range(interval_1[0], interval_1[1]):
            for i2 in range(interval_2[0], interval_2[1]):
                for i3 in range(interval_3[0], interval_3[1]):
                    x = i0 - i2
                    y = i0 - i1
                    z = i0 + i3
                    if x % 2 == 0 and y % 2 == 0 and z % 2 == 0:

                        x = x // 2
                        y = y // 2
                        z = z // 2

                        d0 = x + y + z
                        d1 = x - y + z
                        d2 = y - x + z
                        d3 = z - x - y
                        if (
                            interval_0[0] <= d0 <= interval_0[1]
                            and interval_1[0] <= d1 <= interval_1[1]
                            and interval_2[0] <= d2 <= interval_2[1]
                            and interval_3[0] <= d3 <= interval_3[1]
                        ):
                            # x,y,z are legitimate
                            possible_points.add((x, y, z))

                            md = manhattan((x, y, z))
                            shortest_md = min(shortest_md, md)

    for p in possible_points:
        if manhattan(p) == shortest_md:
            print(p)

    return shortest_md


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
