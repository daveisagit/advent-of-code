"""Advent of code 2015
--- Day 11: Corporate Policy ---
"""

from common.aoc import file_to_string, aoc_part, get_filename
from common.general import window_over


ALPHA_LOWER = "abcdefghijklmnopqrstuvwxyz"


def parse_data(raw_data):
    """Parse the input"""
    data = raw_data
    return data


def char_value(c):
    """Char value"""
    return ord(c) - ord("a")


def digit_to_char(digit):
    """Digit to char"""
    return chr(ord("a") + digit)


def str_base(number, base=26):
    """Convert to string"""
    (d, m) = divmod(number, base)
    if d:
        return str_base(d, base) + digit_to_char(m)
    return digit_to_char(m)


def is_valid(pwd):
    """Password validity"""
    for bc in "oil":
        if bc in pwd:
            return False

    o_pairs = set()
    for w in window_over(pwd, 2):
        if w[0] == w[1]:
            o_pairs.add(w[0])
    if len(o_pairs) < 2:
        return False

    valid = False
    for w in window_over(pwd, 3):
        if w in ALPHA_LOWER:
            valid = True
            break

    if not valid:
        return False

    return True


def next_password(sv, i=1):
    """Get next password"""
    for _ in range(i):
        while True:
            sv += 1
            pwd = str_base(sv)
            if is_valid(pwd):
                break

    return pwd


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    sz = len(data) - 1
    sv = sum(char_value(c) * (26 ** (sz - i)) for i, c in enumerate(data))
    assert str_base(sv) == data

    return next_password(sv)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    sz = len(data) - 1
    sv = sum(char_value(c) * (26 ** (sz - i)) for i, c in enumerate(data))
    assert str_base(sv) == data

    return next_password(sv, i=2)


MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

assert is_valid("abcdffaa")
assert is_valid("ghjaabcc")
assert not is_valid("hijklmmn")
assert not is_valid("abbceffg")

solve_part_a(MY_DATA)

solve_part_b(MY_DATA)
