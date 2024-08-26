"""Advent of code 2023
--- Day 19: Aplenty ---
"""

from collections import deque
from math import prod
import re
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok

PART_NAMES = "xmas"


def parse_data(raw_data):
    """Parse the input
    Return a dict of workflows and list of parts

    A workflow is a list of tests and a default
        A test is an attribute </> value => outcome

    A part is a tuple of attributes

    Attributes are translated to an index(0-3) from xmas
    """

    workflows = {}
    parts = []
    for ln, line in enumerate(raw_data):
        if not line:
            break
        rx = re.search(r"(.+)\{(.+)\}", line)
        wf = rx.group(1)
        conditions = tok(rx.group(2), ",")
        dft = conditions[-1]
        tests = []
        for condition in conditions[:-1]:
            rx = re.search(r"(.)(<|>)(\d+):(.+)", condition)
            condition = (
                PART_NAMES.index(rx.group(1)),
                rx.group(2),
                int(rx.group(3)),
                rx.group(4),
            )
            tests.append(condition)

        workflows[wf] = (tests, dft)

    for line in raw_data[ln:]:
        if not line:
            continue
        arr = tok(line[1:-1], ",")
        part = [0] * 4
        for x in arr:
            rx = re.search(r"(.)=(\d+)", x)
            part[PART_NAMES.index(rx.group(1))] = int(rx.group(2))
        parts.append(tuple(part))

    return workflows, parts


def calc_accepted_ranges(workflows, min=1, max=4001, start="in"):
    """Return a list of accepted ranges, i.e. any part with attributes
    inside all four category ranges is accepted.
    """
    accepted_ranges = []
    ranges = tuple((min, max) for _ in range(4))
    state = start, ranges
    bfs = deque()
    bfs.append(state)
    while bfs:
        state = bfs.popleft()
        wf, ranges = state

        if wf == "R":
            continue

        if wf == "A":
            accepted_ranges.append(ranges)
            continue

        tests, dft = workflows[wf]
        use_default = True

        # new_ranges is the model of the ranges that are left
        # for the next test (or default option)
        # it is updated as we go through pulling out passing sections
        # to pass onto the next workflow
        new_ranges = list(ranges)
        for attr, cmp, val, next_wf in tests:

            # the test fails entirely for the range,
            # carry on to next test
            if (
                cmp == "<"
                and val <= new_ranges[attr][0]
                or cmp == ">"
                and val >= new_ranges[attr][1]
            ):
                continue

            # the test passed entirely for the range,
            # pass onto the next workflow, no more comparisons needed
            if (
                cmp == "<"
                and new_ranges[attr][1] <= val
                or cmp == ">"
                and val <= new_ranges[attr][0]
            ):
                new_state = next_wf, tuple(new_ranges)
                bfs.append(new_state)
                use_default = False
                break

            # the test passes for part of the range,
            # give the passing part to the next workflow
            # leave the remaining section for the remaining tests
            new_ranges_true = new_ranges.copy()
            if cmp == "<":
                new_ranges_true[attr] = new_ranges[attr][0], val
                new_ranges[attr] = val, new_ranges[attr][1]
            else:
                new_ranges_true[attr] = val + 1, new_ranges[attr][1]
                new_ranges[attr] = new_ranges[attr][0], val + 1
            new_state = next_wf, tuple(new_ranges_true)
            bfs.append(new_state)

        # what is left is passed to the default workflow
        # (if applicable)
        if use_default:
            new_state = dft, tuple(new_ranges)
            bfs.append(new_state)

    return accepted_ranges


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    workflows, parts = data
    ranges = calc_accepted_ranges(workflows)
    total = 0
    for part in parts:
        for r in ranges:
            if all(r[i][0] <= x < r[i][1] for i, x in enumerate(part)):
                total += sum(part)
                break
    return total


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    workflows, _ = data
    ranges = calc_accepted_ranges(workflows)
    total = 0
    for r in ranges:
        combinations = prod(b - a for a, b in r)
        total += combinations
    return total


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
