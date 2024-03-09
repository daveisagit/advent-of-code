"""Advent of code 2018
--- Day 14: Chocolate Charts ---
"""

from common.aoc import file_to_list, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        data.append(int(line))
    return data


def iterate(scores: list, e1, e2):
    """Iterate"""
    ns = scores[e1] + scores[e2]
    if ns >= 10:
        scores.append(ns // 10)
    scores.append(ns % 10)
    e1 = e1 + 1 + scores[e1]
    e1 %= len(scores)
    e2 = e2 + 1 + scores[e2]
    e2 %= len(scores)
    return scores, e1, e2


def next_ten_after(r):
    """Find the next 10"""
    scores = [3, 7]
    e1 = 0
    e2 = 1
    while len(scores) < r + 10:
        scores, e1, e2 = iterate(scores, e1, e2)
    nt = scores[r : r + 10]
    return "".join(str(d) for d in nt)


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    for d in data:
        nt = next_ten_after(d)
        print(d, nt)
    return nt


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    data = str(data[0])
    l = len(data)
    scores = [3, 7]
    e1 = 0
    e2 = 1
    while True:
        scores, e1, e2 = iterate(scores, e1, e2)
        last_1 = "".join(str(d) for d in scores[-l:])
        if last_1 == data:
            ans = len(scores) - l
            break

        last_2 = "".join(str(d) for d in scores[-l - 1 : -1])
        if last_2 == data:
            ans = len(scores) - l - 1
            break

    return ans


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(MY_DATA)
