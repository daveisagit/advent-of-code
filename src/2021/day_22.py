"""Advent of code 2021
--- Day 22: Reactor Reboot ---
"""

from bisect import bisect_left
from collections import Counter, defaultdict
from itertools import pairwise
import math
from common.aoc import file_to_list, aoc_part, get_filename
from common.blocks import BlockResolver
from common.general import tok
from blocksets import Block


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


@aoc_part
def solve_part_c(data) -> int:
    """Solve part A"""

    def cross_section_resolver(cross_section):
        state = False
        for _, stack_data in cross_section[::-1]:
            op = stack_data[0]
            if op is True:
                state = not state
                break
            if op is False:
                break

        return state

    br = BlockResolver(3, cross_section_resolver)
    for op, ranges in data:
        a = [0] * 3
        b = [0] * 3
        for d in range(3):
            a[d] = max(ranges[d][0], -50)
            b[d] = min(ranges[d][1], 50) + 1
        block = (tuple(a), tuple(b))
        stack_data = (op,)
        entry = (block, stack_data)
        if all(-50 <= r[0] <= 50 or -50 <= r[1] <= 50 for r in ranges):
            br._operation_stack.append(entry)
    br.resolve()
    total = 0
    for block, stack_data in br._operation_stack:
        x_amt = block[1][0] - block[0][0]
        y_amt = block[1][1] - block[0][1]
        z_amt = block[1][2] - block[0][2]
        total += x_amt * y_amt * z_amt

    return total


@aoc_part
def solve_part_d(data) -> int:
    """Solve part A"""

    def cross_section_resolver(cross_section):
        state = False
        for _, stack_data in cross_section[::-1]:
            op = stack_data[0]
            if op is True:
                state = not state
                break
            if op is False:
                break

        return state

    br = BlockResolver(3, cross_section_resolver)
    for op, ranges in data:
        if any(any(abs(x) <= 50 for x in r) for r in ranges):
            continue
        a = [0] * 3
        b = [0] * 3
        for d in range(3):
            a[d] = ranges[d][0]
            b[d] = ranges[d][1] + 1
        block = (tuple(a), tuple(b))
        stack_data = (op,)
        entry = (block, stack_data)
        br._operation_stack.append(entry)
    print(len(br._operation_stack))
    br.resolve()
    total = 0
    for block, stack_data in br._operation_stack:
        x_amt = block[1][0] - block[0][0]
        y_amt = block[1][1] - block[0][1]
        z_amt = block[1][2] - block[0][2]
        total += x_amt * y_amt * z_amt

    return total


def get_markers(data):
    """Hows the grid divided in terms of blocks"""
    markers = []
    ranges = [r for _, r in data]
    for dim in range(3):
        vals_1 = {x[dim][0] for x in ranges}
        vals_2 = {x[dim][1] for x in ranges}
        vals = vals_1 | vals_2
        vals = sorted(vals)
        markers.append(vals)
    return markers


@aoc_part
def solve_part_e(data) -> int:
    """Solve part A"""
    new_data = []
    for op, ranges in data:
        (ax, bx), (ay, by), (az, bz) = ranges
        if not any(any(abs(x) <= 50 for x in r) for r in ranges):
            continue
        new_row = op, ((ax, bx + 1), (ay, by + 1), (az, bz + 1))
        new_data.append(new_row)
    print(len(new_data))
    markers = get_markers(new_data)
    state = defaultdict(bool)
    for op, ((ax, bx), (ay, by), (az, bz)) in new_data:

        # axi = markers[0].index(ax)
        # bxi = markers[0].index(bx)
        # ayi = markers[1].index(ay)
        # byi = markers[1].index(by)
        # azi = markers[2].index(az)
        # bzi = markers[2].index(bz)

        axi = bisect_left(markers[0], ax)
        bxi = bisect_left(markers[0], bx)
        ayi = bisect_left(markers[1], ay)
        byi = bisect_left(markers[1], by)
        azi = bisect_left(markers[2], az)
        bzi = bisect_left(markers[2], bz)

        for xi in range(axi, bxi):
            for yi in range(ayi, byi):
                for zi in range(azi, bzi):
                    blk = (xi, yi, zi)
                    state[blk] = op

    total = 1134088246458611
    for (xi, yi, zi), ft in state.items():
        if not ft:
            continue
        x_amt = markers[0][xi + 1] - markers[0][xi]
        y_amt = markers[1][yi + 1] - markers[1][yi]
        z_amt = markers[2][zi + 1] - markers[2][zi]
        total += x_amt * y_amt * z_amt

    return total


@aoc_part
def solve_part_f(data) -> int:
    """Solve part A"""
    new_data = []
    for op, ranges in data:
        (ax, bx), (ay, by), (az, bz) = ranges
        new_row = op, (ax, ay, az), (bx + 1, by + 1, bz + 1)
        new_data.append(new_row)

    cubes = Counter()
    for op, a, b in new_data:
        block = Block(a, b)
        update = Counter()
        for c, s in cubes.items():
            i = block & c
            if i is None:
                continue
            update[i.norm] -= s
        if op:
            update[block.norm] += 1
        cubes.update(update)

    return sum(s * (Block.parse(b)).measure for b, s in cubes.items())


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)


MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)


# solve_part_a(EX_DATA)
# solve_part_a(MY_DATA)
solve_part_b(EX_DATA)
# solve_part_b(MY_DATA) # 130s

# solve_part_c(EX_DATA)
# solve_part_d(MY_DATA)  # 310s
# solve_part_e(MY_DATA)  # 200s

solve_part_f(EX_DATA)  # 310s
