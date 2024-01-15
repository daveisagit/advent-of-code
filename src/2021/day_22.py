"""Advent of code 2021
--- Day 22: Reactor Reboot ---
"""

from itertools import pairwise
import math
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        arr = tok(line)
        state = arr[0] == "on"
        arr = tok(arr[1], ",")
        ranges = []
        for cr in arr:
            arr2 = tok(cr, "=")
            arr2 = tok(arr2[1], "..")
            ranges.append(tuple([int(v) for v in arr2]))
        data.append((state, tuple(ranges)))

    return data


# naive approach for part A
# works in under 1s but part B improves that

# def set_of_points(box):
#     box_set = set()

#     def trim_value(val, trim=0):
#         if trim:
#             if val < -trim:
#                 val = -trim
#             elif val > trim:
#                 val = trim
#         return val

#     if box[0][0] > 50 or box[1][0] > 50 or box[2][0] > 50:
#         return set()
#     if box[0][1] < -50 or box[1][1] < -50 or box[2][1] < -50:
#         return set()

#     for x in range(trim_value(box[0][0], 50), trim_value(box[0][1], 50) + 1):
#         for y in range(trim_value(box[1][0], 50), trim_value(box[1][1], 50) + 1):
#             for z in range(trim_value(box[2][0], 50), trim_value(box[2][1], 50) + 1):
#                 box_set.add((x, y, z))
#     return box_set


# @aoc_part
# def solve_part_a(data) -> int:
#     """Solve part A"""
#     all_points = set()
#     for inc, box in data:
#         box_set = set_of_points(box)
#         if inc:
#             all_points.update(box_set)
#             continue
#         all_points.difference_update(box_set)

#     return len(all_points)


def combine_blocks(a: list, b: list) -> list:
    """A block is a list of dimension pairs (Bx,B'x), (By,B'y), (Bz,B'z)
    where B and B' are the opposite corners. Each pair is like a side of a block.
    The return is a set of blocks which represent the resulting possible workspace
    The client of this function can then determine the relevance of each
    within its own context.
    """
    result = []
    grid_markers = [sorted(set(list(sides[0]) + list(sides[1]))) for sides in zip(a, b)]
    dimensions = len(grid_markers)

    def iterate_dimension(other_sides: list):
        cur_depth = len(other_sides)
        markers = grid_markers[cur_depth]
        for side in pairwise(markers):
            new_list_of_sides = other_sides + [side]
            if cur_depth < dimensions - 1:
                iterate_dimension(new_list_of_sides)
                continue
            result.append(tuple(new_list_of_sides))

    iterate_dimension([])

    return result


def intersection_block(a: list, b: list) -> list:
    """Intersection: of the workspace which new sub blocks are in a and b
    Should be 1 or 0 in theory?"""
    result = []
    for c in combine_blocks(a, b):
        c_inside_a = all(
            a_side[0] <= c_side[0] and c_side[1] <= a_side[1]
            for a_side, c_side in zip(a, c)
        )
        c_inside_b = all(
            b_side[0] <= c_side[0] and c_side[1] <= b_side[1]
            for b_side, c_side in zip(b, c)
        )
        if c_inside_a and c_inside_b:
            result.append(c)
    return result


def diff_blocks(a: list, b: list) -> list:
    """Difference a-b: of the workspace which new sub blocks are in a but not b"""
    result = []
    for c in combine_blocks(a, b):
        c_inside_a = all(
            a_side[0] <= c_side[0] and c_side[1] <= a_side[1]
            for a_side, c_side in zip(a, c)
        )
        c_inside_b = all(
            b_side[0] <= c_side[0] and c_side[1] <= b_side[1]
            for b_side, c_side in zip(b, c)
        )
        if c_inside_a and not c_inside_b:
            result.append(c)
    return result


def get_block(box, trim=0):
    """Prepare the box to make a block
    This means adding 1 to the upper ordinate to work with our
    block specification and applying any trim as for part A"""
    res = []
    for side in box:
        a = side[0]
        b = side[1]
        if trim:
            # exclude blocks outside the trim range
            if a > trim or b < -trim:
                return None
            a = max(a, -trim)
            b = min(b, trim)
        res.append((a, b + 1))
    return tuple(res)


def solve(data, trim=0) -> int:
    """Solve: Processing a block means:
    Check for overlapping existing blocks
    For each one with an intersection remove it and replace with the difference.
    This will have the effect of re-constructing a new granular workspace
    for the existing block whilst leaving a gap for the new addition."""

    # Find the first valid "On" block as initial offs can be ignored
    start_with = 0
    for start_with, (inc, box) in enumerate(data):
        block = get_block(box, trim=trim)
        if block and inc:
            break

    # empty space
    current_universe = set()

    for inc, box in data[start_with:]:
        block = get_block(box, trim=trim)
        if not block:
            continue

        for existing_block in list(current_universe):
            if intersection_block(existing_block, block):
                # always diff not a union for On
                # we want to put back the existing block
                # in its new sub-block form but with the new block missing
                replacement_blocks = set(diff_blocks(existing_block, block))
                current_universe.remove(existing_block)
                current_universe.update(replacement_blocks)
                # we only need to fill the space for the addition
                # if this is an "On" block

        if inc:
            current_universe.add(block)

    total = 0
    for block in current_universe:
        lengths = [(side[1] - side[0]) for side in block]
        vol = math.prod(lengths)
        total += vol

    return total


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    return solve(data, trim=50)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    return solve(data, trim=0)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)


MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)


solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
