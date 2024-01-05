"""Advent of code 2021
--- Day 10: Syntax Scoring ---
"""

from collections import deque
from common.aoc import file_to_list, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    data = raw_data
    return data


brace_points = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

brace_pairs = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}

brace_points_b = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def illegal(line):
    """Return the illegal brace or the stack remains"""
    stk = deque()
    for c in line:
        if c in brace_pairs:
            stk.append(brace_pairs[c])
        else:
            if stk:
                expected = stk.pop()
                if c != expected:
                    return True, c
            else:
                return True, c
    complete = [*stk][::-1]
    return False, complete


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    points = 0
    for line in data:
        is_illegal, brace = illegal(line)
        if is_illegal:
            points += brace_points[brace]
    return points


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    scores = []
    for line in data:
        is_illegal, braces = illegal(line)
        if not is_illegal:
            score = 0
            for c in braces:
                score *= 5
                score += brace_points_b[c]
            scores.append(score)
    scores = sorted(scores)
    mid_val = scores[len(scores) // 2]
    return mid_val


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
