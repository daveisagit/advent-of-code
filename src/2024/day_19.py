"""Advent of code 2024
--- Day 19: Linen Layout ---
"""

from functools import lru_cache

from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    patterns = tok(raw_data[0], ",")
    designs = raw_data[2:]
    return patterns, designs


def string_composition_exists(components, full_string: str):
    """Returns True if possible to make the full string from components
    Uses memoize for efficiency
    """

    @lru_cache(maxsize=None)
    def recurrence(s):
        if s == "":
            return True
        for cmp in components:
            l = len(cmp)
            if s[:l] == cmp:
                if recurrence(s[l:]):
                    return True
        return False

    return recurrence(full_string)


def string_composition_count(components, full_string: str, just_existence=False):
    """Returns the ways to make the full string using the components
    Uses memoize for efficiency
    """

    @lru_cache(maxsize=None)
    def recurrence(s):
        if s == "":
            return 1
        cnt = 0
        for cmp in components:
            l = len(cmp)
            if s[:l] == cmp:
                cnt += recurrence(s[l:])
        return cnt

    return recurrence(full_string)


def generate_string_composition_combinations(components, full_string: str):
    """Generator for the actual ways to make the full string using the components"""

    def recurrence(s):
        for cmp in components:
            l = len(cmp)
            if s[:l] == cmp:
                if s[l:] != "":
                    for way in recurrence(s[l:]):
                        yield (cmp,) + way
                else:
                    yield (cmp,)

    yield from recurrence(full_string)


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    patterns, designs = data
    cnt = 0
    for d in designs:
        if string_composition_exists(patterns, d):
            cnt += 1

    return cnt


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    patterns, designs = data
    cnt = 0
    for d in designs:
        cnt += string_composition_count(patterns, d)
    return cnt


@aoc_part
def solve_part_c(data) -> int:
    """Solve part C"""
    patterns, designs = data
    for d in designs:
        print()
        print(f"{d}")
        for composition in generate_string_composition_combinations(patterns, d):
            print(composition)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)

# solve_part_c(EX_DATA)
