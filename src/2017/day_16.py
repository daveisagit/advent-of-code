"""Advent of code 2017
--- Day 16: Permutation Promenade ---
"""

from common.aoc import aoc_part, file_to_string, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    arr = tok(raw_data, ",")
    data = []
    for a in arr:
        move = a[0]
        if move == "s":
            args = int(a[1:])
        if move == "x":
            args = tuple(int(x) for x in tok(a[1:], "/"))
        if move == "p":
            args = tuple(x for x in tok(a[1:], "/"))
        data.append((move, args))

    return data


def get_starting_line(sz):
    """Starting line"""
    c = ord("a")
    s = []
    for x in range(c, c + sz):
        s.append(chr(x))
    return s


def do_dance(data, line):
    """Do your dance"""
    sz = len(line)
    for m, args in data:
        if m == "s":
            line = line[sz - args :] + line[: sz - args]
        if m == "x":
            line[args[0]], line[args[1]] = line[args[1]], line[args[0]]
        if m == "p":
            a = line.index(args[0])
            b = line.index(args[1])
            line[a], line[b] = line[b], line[a]

    return line


@aoc_part
def solve_part_a(data, sz=5) -> int:
    """Solve part A"""
    line = get_starting_line(sz)
    line = do_dance(data, line)
    return "".join(line)


def find_repeat(data, sz):
    """Find the repeat"""
    line = get_starting_line(sz)
    s = "".join(line)
    outcomes = [s]
    n = 0
    while True:
        n += 1
        line = do_dance(data, line)
        s = "".join(line)
        if s in outcomes:
            p = outcomes.index(s)
            return p, n, outcomes
        outcomes.append(s)


@aoc_part
def solve_part_b(data, sz=5) -> int:
    """Solve part B"""
    after = 1000000000
    a, b, outcomes = find_repeat(data, sz)
    m = b - a
    cc = (after - a) % m
    pos = outcomes[cc + a]
    return pos


EX_RAW_DATA = file_to_string(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)


MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA, sz=16)

solve_part_b(MY_DATA, sz=16)
