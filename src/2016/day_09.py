"""Advent of code 2016
--- Day 9: Explosives in Cyberspace ---
"""

import re
from common.aoc import file_to_list, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    data = raw_data
    return data


def decompress_once(s):
    """Iteration of decompress
    Regex trick ^[^\(]* forces first find of (AxB)
    ^     : force start from the start
    [^\(] : match to any non bracket (
    So ^[^\(]* is everything before the first find of (AxB)
    """
    rr = re.search(r"(^[^\(]*)\((\d+)x(\d+)\)(.*)", s)
    if rr is None:
        return s, ""
    before = rr.group(1)
    nxt_len = int(rr.group(2))
    rpt_amt = int(rr.group(3))
    remain = rr.group(4)
    nxt = remain[:nxt_len]
    nxt *= rpt_amt
    remain = remain[nxt_len:]
    ns = before + nxt
    return ns, remain


def decompress(s):
    """As per puzzle"""
    remain = s
    res = ""
    while remain != "":
        ns, remain = decompress_once(remain)
        res += ns
    return res


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""

    for s in data:
        ns = decompress(s)
        if len(data) > 1:
            print(f"{s:20} {ns:20} {len(ns)} ")

    return len(ns)


def decompress_to_size(s):
    """Use recursion to resolve the length"""
    rr = re.search(r"(^[^\(]*)\((\d+)x(\d+)\)(.*)", s)
    if rr is None:
        return len(s)
    before = rr.group(1)
    nxt_len = int(rr.group(2))
    rpt_amt = int(rr.group(3))
    remain = rr.group(4)
    nxt = remain[:nxt_len]
    remain = remain[nxt_len:]

    length = (
        len(before) + rpt_amt * decompress_to_size(nxt) + decompress_to_size(remain)
    )

    return length


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    for s in data:
        l = decompress_to_size(s)
        if len(data) > 1:
            print(f"{s:20} {l}")

    return l


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
