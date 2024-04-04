"""Advent of code 2017
--- Day 25: The Halting Problem ---
"""

from collections import defaultdict
import re
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import window_over


def parse_data(raw_data):
    """Parse the input"""
    start_state = raw_data[0][-2]
    rr = re.search(r".+\s(\d+)\s.+", raw_data[1])
    steps = int(rr.group(1))

    states = defaultdict(list)
    for state_lines in window_over(raw_data[3:], 9, 10):
        state_id = state_lines[0][-2]

        for offset in range(2):
            offset *= 4
            rr = re.search(r".+\s(\d+).", state_lines[2 + offset])
            w = int(rr.group(1))
            m = 1
            if state_lines[3 + offset][-5:] == "left.":
                m = -1
            ns = state_lines[4 + offset][-2]

            states[state_id].append((w, m, ns))

    return start_state, steps, states


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    current_state_id, steps, states = data
    tape = defaultdict(int)
    cursor = 0
    for _ in range(steps):
        current_value = tape[cursor]
        w, m, ns = states[current_state_id][current_value]
        tape[cursor] = w
        cursor += m
        current_state_id = ns

    ans = sum(v for v in tape.values() if v == 1)

    return ans


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    return len(data)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)
