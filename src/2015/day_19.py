"""Advent of code 2015
--- Day 19: Medicine for Rudolph ---
"""

from heapq import heappop, heappush
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok, window_over


def parse_data(raw_data):
    """Parse the input"""
    data = []
    ln = 0
    for ln, line in enumerate(raw_data):
        if not line:
            break
        arr = tok(line, "=>")
        data.append(tuple(arr))
    mm = raw_data[ln + 1]
    return data, mm


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    reps, mm = data
    molecules = set()
    for f, r in reps:
        indexes = [i for i, w in enumerate(window_over(mm, len(f))) if w == f]
        for i in indexes:
            s = mm[:i] + r + mm[i + len(f) :]
            molecules.add(s)
    return len(molecules)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B
    Go backwards start from mm and stop at e
    Make the string size the priority on the heap"""
    reps, mm = data
    state = len(mm), 0, mm
    h = []
    heappush(h, state)
    while h:
        state = heappop(h)
        sz, steps, m = state
        # print(m)

        if m == "e":
            return steps

        for f, r in reps:
            indexes = [i for i, w in enumerate(window_over(m, len(r))) if w == r]
            for i in indexes:
                s = m[:i] + f + m[i + len(r) :]
                state = len(s), steps + 1, s
                heappush(h, state)

    return None


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(MY_DATA)
