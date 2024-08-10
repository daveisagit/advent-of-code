"""Advent of code 2022
--- Day 21: Monkey Math ---
"""

from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    data = {}
    for row in raw_data:
        arr = tok(row, ":")
        left = arr[0]
        right = arr[1]

        try:
            val = int(right)
        except ValueError:
            val = tuple(tok(right))

        data[left] = val

    return data


def get_value(monkey, table, known):
    """Find the answer for a monkey and memoize it over recursion"""
    if monkey in known:
        return known[monkey]
    val = table[monkey]
    if isinstance(val, int):
        known[monkey] = val
        return val

    left = get_value(val[0], table, known)
    right = get_value(val[2], table, known)
    op = val[1]
    if op == "+":
        ans = left + right
    elif op == "-":
        ans = left - right
    elif op == "*":
        ans = left * right
    elif op == "/":
        ans = left / right
    else:
        raise ValueError("Bad Op")
    known[monkey] = ans
    return ans


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    r = get_value("root", data, {})
    assert r == int(r)
    return int(r)


def get_diff(data, human_value):
    """Return left - right for a given human value"""
    expr = data["root"]
    left = expr[0]
    right = expr[2]
    data["humn"] = human_value
    known = {}
    lv = get_value(left, data, known)
    rv = get_value(right, data, known)
    return lv - rv


def binary_search(data, start, forward=True):
    """The result is linear so we can do a binary search"""
    r = get_diff(data, start)
    if r == 0:
        return start

    positive = True if r > 0 else False
    inc = 1
    if not forward:
        inc = -1

    while True:
        v = inc + start
        r = get_diff(data, v)
        if r == 0:
            return v
        if positive and r > 0 or not positive and r < 0:
            inc *= 2
        else:
            break

    return binary_search(data, v, forward=not forward)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    return binary_search(data, 0)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
