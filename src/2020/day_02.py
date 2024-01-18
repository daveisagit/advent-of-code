"""Advent of code 2020
--- Day 2: Password Philosophy ---
"""

from collections import Counter, namedtuple
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok

PP = namedtuple("PP", ("low", "upp", "ch", "pwd"))


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        arr = tok(line)
        pwd = arr[2]
        rng = arr[0]
        arr = tok(arr[1], ":")
        ch = arr[0]
        arr = tok(rng, "-")
        rng = tuple(int(v) for v in arr)
        data.append(PP(rng[0], rng[1], ch, pwd))
    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    total = 0
    for pp in data:
        pp: PP
        cnt = Counter(pp.pwd)
        if pp.ch in pp.pwd and pp.low <= cnt[pp.ch] <= pp.upp:
            total += 1

    return total


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""

    def ch_found(pos):
        pos -= 1
        return pos < len(pp.pwd) and pp.pwd[pos] == pp.ch

    total = 0
    for pp in data:
        pp: PP
        if ch_found(pp.low) != ch_found(pp.upp):
            total += 1

    return total


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
