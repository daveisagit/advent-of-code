"""Advent of code 2020
--- Day 6: Custom Customs ---
"""

from collections import Counter
from common.aoc import file_to_list, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    data = []
    group = []
    for line in raw_data:
        if not line:
            data.append(group)
            group = []
            continue
        group.append(line)
    data.append(group)
    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    group_yes = []
    for group in data:
        group_questions = set()
        for line in group:
            cnt = Counter(line)
            questions = set(cnt)
            group_questions.update(questions)
        group_yes.append(len(group_questions))
    return sum(group_yes)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    group_yes = []
    for group in data:
        group_questions = set(chr(i) for i in range(97, 97 + 26))
        for line in group:
            cnt = Counter(line)
            questions = set(cnt)
            group_questions.intersection_update(questions)
        group_yes.append(len(group_questions))
    return sum(group_yes)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
