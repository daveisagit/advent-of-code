"""Advent of code 2017
--- Day 13: Packet Scanners ---
"""

from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    data = {}
    for line in raw_data:
        arr = [int(a) for a in tok(line, ":")]
        data[arr[0]] = arr[1]
    return data


def get_severity(data):
    """Return the severity of the delay"""
    s = 0
    for t in range(max(data) + 1):

        if t not in data:
            continue

        r = data[t]
        if r == 2:
            p = t % 2
        else:
            d = 2 * -((t // (r - 1)) % 2) + 1
            a = (t % (r - 1)) * d
            e = 0 if d == 1 else r - 1
            p = e + a

        if p == 0:
            s += t * r

    return s


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    return get_severity(data)


def caught(data, delay=0):
    """Return the severity of the delay"""
    for layer in range(max(data) + 1):

        if layer not in data:
            continue

        t = layer + delay
        r = data[layer]
        if r == 2:
            p = t % 2
        else:
            d = 2 * -((t // (r - 1)) % 2) + 1
            a = (t % (r - 1)) * d
            e = 0 if d == 1 else r - 1
            p = e + a

        if p == 0:
            return True

    return False


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    delay = 0
    while True:
        delay += 1
        if not caught(data, delay=delay):
            return delay


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
