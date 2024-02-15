"""Advent of code 2019
--- Day 16: Flawed Frequency Transmission ---
"""

from common.aoc import aoc_part, file_to_string, get_filename


def parse_data(raw_data):
    """Parse the input"""
    return [int(c) for c in raw_data]


def get_repeating_patterns(data):
    """Determine all the patterns up front"""
    sz = len(data)
    base = [0, 1, 0, -1]
    patterns = []
    for idx in range(1, len(data) + 1):
        pattern = []
        while len(pattern) <= len(data):
            for x in base:
                xr = [x] * idx
                pattern.extend(xr)
        pattern = pattern[1 : sz + 1]
        patterns.append(pattern)
    return patterns


def iterate(patterns, data):
    """Iterate"""
    new_data = []
    for p in patterns:
        x = abs(sum(a * b for a, b in zip(p, data)))
        x %= 10
        new_data.append(x)
    return new_data


def to_str(data, first=None):
    """Visualize"""
    s = "".join(str(x) for x in data)
    if first is not None:
        s = s[:first]
    return s


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    patterns = get_repeating_patterns(data)
    for _ in range(100):
        data = iterate(patterns, data)
    return to_str(data, 8)


def get_repeat_of_size(data, size):
    """Get config for a given repeated input"""
    new_data = data * size
    patterns = get_repeating_patterns(new_data)
    return new_data, patterns


def last_n_digits_match(a, b):
    """How many digits match in the tail"""
    i = 1
    while True:
        if a[-i] != b[-i]:
            return i - 1
        i += 1


def digits_at(data, phase, pos, length):
    """Returns the digits for a given position in phase for
    when pos > size / 2
    """
    cur = data[pos:]
    for _ in range(phase):
        total = 0
        for i in range(len(cur) - 1, -1, -1):
            total += cur[i]
            cur[i] = total % 10
    return cur[:length]


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""

    # Pascals triangle from top right for digits in the
    # second half, demo for example

    if len(data) < 100:
        ex_data = [1, 2, 3, 4, 5, 6, 7, 8] * 4
        patterns = get_repeating_patterns(ex_data)
        for i in range(100):
            ex_data = iterate(patterns, ex_data)
            if i < 10:
                print(to_str(ex_data))
        print("...")
        print(to_str(ex_data))

        ex_data = [1, 2, 3, 4, 5, 6, 7, 8] * 4
        t = to_str(digits_at(ex_data, 100, len(ex_data) - 8, 8))
        print(t)

    p = int(to_str(data, 7))
    data = data * 10000
    t = to_str(digits_at(data, 100, p, 8))
    return t


EX_RAW_DATA = file_to_string(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
