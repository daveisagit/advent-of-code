"""Advent of code 2017
--- Day 6: Memory Reallocation ---
"""

from collections import defaultdict
from common.aoc import aoc_part, file_to_string, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    return tuple(int(x) for x in tok(raw_data))


def next_state(state):
    """Return the next state"""
    new_state = list(state)
    cnt = len(state)
    highest = max(state)
    share_idx = [i for i, b in enumerate(state) if b == highest][0]
    share_amt = state[share_idx]
    at_least = share_amt // cnt
    bonus = share_amt % cnt
    new_state[share_idx] = 0
    for i in range(cnt):
        idx = (share_idx + i + 1) % cnt
        new_state[idx] += at_least
        if i < bonus:
            new_state[idx] += 1
    return tuple(new_state)


@aoc_part
def solve_part_a(state) -> int:
    """Solve part A"""
    states = {state}
    while True:
        state = next_state(state)
        if state in states:
            break
        states.add(state)

    return len(states)


@aoc_part
def solve_part_b(state) -> int:
    """Solve part B"""
    states = defaultdict(list)
    c = 0
    while True:
        states[state].append(c)
        if len(states[state]) > 1:
            return states[state][1] - states[state][0]
        state = next_state(state)
        c += 1


EX_RAW_DATA = file_to_string(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
