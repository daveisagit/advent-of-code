"""Advent of code 2018
--- Day 23: Experimental Emergency Teleportation ---
"""

from collections import defaultdict
from itertools import pairwise, product
from math import inf
from operator import sub
import re
from common.aoc import file_to_list, aoc_part, get_filename
from common.blocks import BlockResolver, BlockResolverUsingBlock
from common.grid_3d import octahedron_manhattan_planes, octaplanes_to_point_set
from blocksets import Block


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
    parallel planes. Each entry is a 4-tuple of the manhattan ranges.
    Use the pythonic standard on expressing the upper limit as exclusive"""
    pp = []
    for nb in data:
        x, y, z, d = nb
        pd = [x + y, x - y, y - x, -x - y]
        pd = [p + z for p in pd]
        pd = [(p - d, p + d + 1) for p in pd]
        pp.append(tuple(pd))
    return pp


# Naive attempt to compute the cartesian product of the intervals

# def get_intersections(spaces):
#     """Return a set of the intersections of all the spaces"""

#     def intersect(spa, spb):
#         spc = []
#         for i in range(4):
#             a_from, a_to = spa[i]
#             b_from, b_to = spb[i]
#             c_from = max(a_from, b_from)
#             c_to = min(a_to, b_to)
#             d = c_to - c_from
#             if d > 0:
#                 spc.append((c_from, c_to))
#             else:
#                 spc.append(None)
#         return spc

#     result = set()
#     for cnt, (spa, spb) in enumerate(combinations(spaces, 2)):
#         # if cnt % 10000 == 0:
#         #     print(cnt, len(result))
#         spc = intersect(spa, spb)
#         if not all(spc):
#             continue
#         result.add(tuple(spc))
#     return result


def get_range_memberships(spaces):
    """Return membership of indexes to ranges
    A list of dimensions, in each dimension a dictionary of
    range (manhattan) : set of nanobots
    """

    def for_dimension(dim):
        range_membership_for_dim = defaultdict(set)
        spaces_for_dim = [b[dim] for b in spaces]
        values = sorted(
            list({sp[0] for sp in spaces_for_dim} | {sp[1] for sp in spaces_for_dim})
        )
        for a, b in pairwise(values):
            for idx, dim_space in enumerate(spaces_for_dim):
                p, q = dim_space
                if max(a, p) < min(b, q):
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
    # a space is a set of 4 manhattan ranges
    spaces = get_parallel_planes(data)

    # split the 4 "diagonal vectors" into intervals
    # and find out which nanobots occupy each interval
    range_memberships = get_range_memberships(spaces)

    # checking the cartesian product for every possible sub-space
    # is too long about 2000^4
    # So instead read the each dimension by popularity, i.e. focus on the central
    # cluster where most of the nanobots are
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
                            f"# bots = {len(indexes)} within ALL 4 manhattan plane ranges {sweet_spot}"
                        )

    # now that we know the manhattan ranges for the 4 directions (8 bounding planes)
    # which is is closest to the origin?
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
                            interval_0[0] <= d0 < interval_0[1]
                            and interval_1[0] <= d1 < interval_1[1]
                            and interval_2[0] <= d2 < interval_2[1]
                            and interval_3[0] <= d3 < interval_3[1]
                        ):
                            # x,y,z are legitimate
                            possible_points.add((x, y, z))

                            md = manhattan((x, y, z))
                            shortest_md = min(shortest_md, md)

    for p in possible_points:
        if manhattan(p) == shortest_md:
            print(p)

    return shortest_md


@aoc_part
def solve_part_c(data) -> int:
    """Solve part B using BlockResolver"""

    # get the octaplanes
    pp = [octahedron_manhattan_planes((x, y, z), d) for x, y, z, d in data]

    # convert 4 pairs of planes to a 4D block
    pp = [tuple(zip(*x)) for x in pp]
    br = BlockResolverUsingBlock(4, None)

    for a, b in pp:
        blk = Block(a, b)
        br._operation_stack.append((blk, 1))

    br._refresh_marker_ordinates()
    br._refresh_marker_stack()
    most_intersected = br.most_intersected_segments()

    # the most i.e. top 1 = first, ignore the value
    most_intersected_segment, _ = most_intersected[0]

    # convert markers back to actual ordinates
    most_intersected_region = tuple(
        (br._marker_ordinates[d][x], br._marker_ordinates[d][x + 1])
        for d, x in enumerate(most_intersected_segment)
    )
    print(most_intersected_region)

    # translate the region defined to a set of points
    p = octaplanes_to_point_set(most_intersected_region)
    print(p)

    # the 1st parallel plane range is the x+y value
    # i.e. the manhattan distance
    # so no need to translate pp back to xy
    # for the answer
    return br._marker_ordinates[0][most_intersected_segment[0]]


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)

solve_part_c(MY_DATA)
