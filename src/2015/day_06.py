"""Advent of code 2015
--- Day 6: Probably a Fire Hazard ---
"""

from collections import Counter, defaultdict, deque
import re
from common.aoc import file_to_list, aoc_part, get_filename
from common.blocks import BlockResolver, BlockResolverUsingBlock
from blocksets import Block


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        rr = re.search(
            r"(turn off|turn on|toggle) (\d+),(\d+) through (\d+),(\d+)", line
        )
        op = rr.group(1)
        vals = [int(v) for v in rr.groups()[1:]]
        a = (vals[0], vals[1])
        b = (vals[2] + 1, vals[3] + 1)
        data.append((op, a, b))
    return data


def get_markers(data):
    """Hows the grid divided in terms of blocks"""
    markers = []
    for dim in range(2):
        vals_1 = {x[1][dim] for x in data}
        vals_2 = {x[2][dim] for x in data}
        vals = vals_1 | vals_2
        vals.update({0, 1000})
        vals = sorted(vals)
        markers.append(vals)
    return markers


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    markers = get_markers(data)
    state = defaultdict(bool)
    for op, (ax, ay), (bx, by) in data:

        axi = markers[0].index(ax)
        bxi = markers[0].index(bx)
        ayi = markers[1].index(ay)
        byi = markers[1].index(by)

        for xi in range(axi, bxi):
            for yi in range(ayi, byi):
                blk = (xi, yi)
                if op == "turn on":
                    state[blk] = True
                if op == "turn off":
                    state[blk] = False
                if op == "toggle":
                    state[blk] = not state[blk]

    total = 0
    for (xi, yi), ft in state.items():
        if not ft:
            continue
        x_amt = markers[0][xi + 1] - markers[0][xi]
        y_amt = markers[1][yi + 1] - markers[1][yi]
        total += x_amt * y_amt

    return total


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    markers = get_markers(data)
    state = defaultdict(int)
    for op, (ax, ay), (bx, by) in data:

        axi = markers[0].index(ax)
        bxi = markers[0].index(bx)
        ayi = markers[1].index(ay)
        byi = markers[1].index(by)

        for xi in range(axi, bxi):
            for yi in range(ayi, byi):
                blk = (xi, yi)
                if op == "turn on":
                    state[blk] += 1
                if op == "turn off":
                    if state[blk] > 0:
                        state[blk] -= 1
                if op == "toggle":
                    state[blk] += 2

    total = 0
    for (xi, yi), b in state.items():
        x_amt = markers[0][xi + 1] - markers[0][xi]
        y_amt = markers[1][yi + 1] - markers[1][yi]
        total += b * x_amt * y_amt

    return total


@aoc_part
def solve_part_c(data) -> int:
    """Solve part A - alt"""

    def cross_section_resolver(cross_section):
        state = False
        for _, stack_data in cross_section[::-1]:
            op = stack_data[0]
            if op == "turn on":
                state = not state
                break
            if op == "turn off":
                break
            if op == "toggle":
                state = not state

        return state

    br = BlockResolverUsingBlock(2, cross_section_resolver)
    for op, a, b in data:
        block = Block(a, b)
        stack_data = (op,)
        entry = (block, stack_data)
        br._operation_stack.append(entry)
    br.resolve()

    total = 0
    for block, stack_data in br._operation_stack:
        total += block.measure

    return total


@aoc_part
def solve_part_d(data) -> int:
    """Solve part B - alt"""

    def cross_section_resolver(cross_section):
        state = 0
        for _, stack_data in cross_section:
            op = stack_data[0]
            if op == "turn on":
                state += 1
            if op == "turn off":
                state -= 1
                state = max(0, state)
            if op == "toggle":
                state += 2
        return state

    br = BlockResolverUsingBlock(2, cross_section_resolver)
    for op, a, b in data:
        block = Block(a, b)
        stack_data = (op,)
        entry = (block, stack_data)
        br._operation_stack.append(entry)
    br.resolve()

    total = 0
    for block, stack_data in br._operation_stack:
        total += block.measure * stack_data[0]

    return total


@aoc_part
def solve_part_e(data) -> int:
    """Solve part A"""

    q = deque()
    for x in data:
        q.append(x)

    cubes = Counter()
    while q:
        op, a, b = q.popleft()
        block = Block(a, b)
        update = Counter()

        if op == "toggle":
            update[block] += 1

        for c, s in cubes.items():
            i = block & c
            if i is None:
                continue

            if op == "toggle":
                update[i] -= 2 * s
            else:
                update[i] -= s

        if op == "turn on":
            update[block] += 1

        cubes.update(update)

    return sum(s * b.measure for b, s in cubes.items())


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

# solve_part_a(EX_DATA)
solve_part_a(MY_DATA)
solve_part_b(MY_DATA)

# # using BlockResolver
solve_part_c(MY_DATA)
solve_part_d(MY_DATA)

# part A using set theory, slower due
# to amount of intersection
# solve_part_e(MY_DATA)
