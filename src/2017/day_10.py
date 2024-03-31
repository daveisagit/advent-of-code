"""Advent of code 2017
--- Day 10: Knot Hash ---
"""

from common.aoc import aoc_part, file_to_string, get_filename
from common.general import hex_pad, tok, window_over


def parse_data(raw_data):
    """Parse the input"""
    return [int(x) for x in tok(raw_data, ",")]


def do_hash(data, lst, cp=0, skip=0):
    """Do the hash"""
    sz = len(lst)
    for l in data:

        for i in range(((l + 1) // 2)):
            i1 = (cp + i) % sz
            i2 = (cp - i + l - 1) % sz
            lst[i1], lst[i2] = lst[i2], lst[i1]

        cp += l + skip
        skip += 1
    return lst, cp, skip


@aoc_part
def solve_part_a(data, sz=5) -> int:
    """Solve part A"""
    lst = list(range(sz))
    do_hash(data, lst)
    return lst[0] * lst[1]


def do_hash_b(s):
    """Hash Man!"""
    lst = list(range(256))
    data = [ord(c) for c in s]
    data += [17, 31, 73, 47, 23]
    cp = 0
    skip = 0
    for _ in range(64):
        lst, cp, skip = do_hash(data, lst, cp, skip)

    dense = []
    for block in window_over(lst, 16, 16):
        c = block[0]
        for d in block[1:]:
            c ^= d
        dense.append(c)

    dense = [hex_pad(d, 2) for d in dense]

    return "".join(dense)


@aoc_part
def solve_part_b(raw_data) -> int:
    """Solve part B"""
    return do_hash_b(raw_data)


EX_RAW_DATA = file_to_string(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA, sz=256)
assert solve_part_b("") == "a2582a3a0e66e6e86e3812dcb672a272"
assert solve_part_b("AoC 2017") == "33efeb34ea91902bb2f59c9920caa6cd"
assert solve_part_b("1,2,3") == "3efbe78a8d82f29979031a4aa0b16a9d"
solve_part_b(MY_RAW_DATA)
