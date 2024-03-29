"""Advent of code 2017
--- Day 4: High-Entropy Passphrases ---
"""

from itertools import combinations
from typing import Counter
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        words = tok(line)
        data.append(words)

    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    valid_phrases = []
    for phrase in data:
        cnt = Counter(phrase)
        if cnt.most_common()[0][1] == 1:
            valid_phrases.append(phrase)

    return len(valid_phrases)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    valid_phrases = []
    for phrase in data:
        cnt = Counter(phrase)
        if cnt.most_common()[0][1] != 1:
            continue

        valid = True
        for a, b in combinations(phrase, 2):
            if len(a) != len(b):
                continue
            if sorted(a) == sorted(b):
                valid = False
                break
        if not valid:
            continue

        valid_phrases.append(phrase)

    return len(valid_phrases)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
