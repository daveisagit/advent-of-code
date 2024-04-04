"""Advent of code 2016
--- Day 5: How About a Nice Game of Chess? ---
"""

import hashlib
from common.aoc import file_to_string, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    data = raw_data
    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    i = 0
    pwd = ""
    while True:

        s = f"{data}{i}".encode()
        h = hashlib.md5(s)
        h = h.hexdigest()
        if h[:5] == "00000":
            pwd += h[5]
            if len(pwd) == 8:
                break
        i += 1

    return pwd


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    i = 0
    pwd = [" "] * 8
    while True:

        s = f"{data}{i}".encode()
        h = hashlib.md5(s)
        h = h.hexdigest()
        if h[:5] == "00000":
            p = h[5]
            v = h[6]
            if p in "01234567":
                p = int(p)
                if pwd[p] == " ":
                    pwd[p] = v
                    print("".join(pwd))
                    if " " not in pwd:
                        pwd = "".join(pwd)
                        return pwd

        i += 1


EX_RAW_DATA = file_to_string(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
