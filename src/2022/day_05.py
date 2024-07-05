"""Advent of code 2022
--- Day 5: Supply Stacks ---
"""

from copy import deepcopy
import re
from common.aoc import (
    aoc_part,
    file_to_list_no_strip_2,
    get_filename,
)


def parse_data(raw_data):
    """Parse the input"""
    stacks = []
    for i, line in enumerate(raw_data):

        if not stacks:
            stack_count = (len(line) + 1) // 4
            for _ in range(stack_count):
                stacks.append([])

        if line[1] == "1":
            break
        stack_data = line[1::4]
        for stk, ch in enumerate(stack_data):
            if ch != " ":
                stacks[stk].append(ch)

    moves = []
    for line in raw_data[i + 2 :]:
        rr = re.search(r"move (\d+) from (\d+) to (\d+)", line)
        move = [int(x) for x in rr.groups()]
        moves.append(move)

    return stacks, moves


def crate_mover(stacks, moves, part_b=False):
    for m, f, t in moves:
        f -= 1
        t -= 1
        move = stacks[f][:m]
        stacks[f] = stacks[f][m:]
        if not part_b:
            move = list(reversed(move))
        stacks[t] = move + stacks[t]


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    stacks, moves = data
    stacks = deepcopy(stacks)
    crate_mover(stacks, moves)
    tops = [stack[0] for stack in stacks]
    return "".join(tops)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    stacks, moves = data
    stacks = deepcopy(stacks)
    crate_mover(stacks, moves, part_b=True)
    tops = [stack[0] for stack in stacks]
    return "".join(tops)


EX_RAW_DATA = file_to_list_no_strip_2(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list_no_strip_2(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
