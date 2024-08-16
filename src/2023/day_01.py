"""Advent of code 2023
--- Day 1: Trebuchet?! ---
"""

from common.aoc import file_to_list, aoc_part, get_filename

digits_as_words = [
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]


def parse_data(raw_data):
    """Parse the input"""
    return raw_data


def get_first_digit(s: str) -> int | None:
    """Return the first digit found in a string"""
    for c in s:
        if c.isdigit():
            return int(c)
    return None


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    return sum(
        get_first_digit(line) * 10 + get_first_digit(line[::-1]) for line in data
    )


def translate_line(line: str, reverse=False) -> str:
    """Translate the first (or last) digit word found to a digit.
    Set the reverse argument to True to find the last.
    """
    if reverse:
        line = line[::-1]
    closest = len(line)
    first_digit = None
    for idx, word in enumerate(digits_as_words):
        if reverse:
            word = word[::-1]
        try:
            found_at = line.index(word)
            if found_at < closest:
                closest = found_at
                first_digit = idx
        except ValueError:
            pass

    # first_digit is the index of digits_as_words
    # we swap out the text for the digit character
    if first_digit is not None:
        look_for = digits_as_words[first_digit]
        if reverse:
            look_for = look_for[::-1]
        line = line.replace(look_for, str(first_digit + 1), 1)

    if reverse:
        line = line[::-1]

    return line


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    total = 0
    for line in data:
        line_1 = translate_line(line)
        line_2 = translate_line(line, reverse=True)
        num = get_first_digit(line_1) * 10 + get_first_digit(line_2[::-1])
        total += num
    return total


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

EX_RAW_DATA = file_to_list(get_filename(__file__, "xb"))
EX_DATA = parse_data(EX_RAW_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
