"""Advent of code 2016
--- Day 14: One-Time Pad ---
"""

from collections import Counter, defaultdict
import hashlib
from common.aoc import file_to_string, aoc_part, get_filename
from common.general import window_over


def parse_data(raw_data):
    """Parse the input"""
    data = raw_data
    return data


def contains_bunch(s, sz=3):
    """Return the first bunch found of n chars the same"""
    for w in window_over(s, sz):
        cnt = Counter(w)
        if len(cnt) == 1:
            return w
    return None


def find_keys(salt, start=0, stretch=0):
    """Generator for keys"""

    def hash_iter(salt, t=stretch):
        s = f"{salt}{i}".encode()
        h = hashlib.md5(s)
        h = h.hexdigest()
        for _ in range(t):
            bs = h.encode()
            h = hashlib.md5(bs)
            h = h.hexdigest()
        return h

    i = start
    bunches = defaultdict(list)
    while True:
        h = hash_iter(salt)

        b = contains_bunch(h, sz=5)
        if b:
            prv = bunches.get(b[2:])
            prv = [p for p in prv if p + 1000 >= i]
            for p in prv:
                yield p

        b = contains_bunch(h)
        if b:
            bunches[b].append(i)

        i += 1


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    keys = []
    for idx in find_keys(data, stretch=0):
        keys.append(idx)
        if len(keys) >= 70:
            break
    keys = sorted(keys)
    return keys[63]


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    keys = []
    for idx in find_keys(data, stretch=2016):
        keys.append(idx)
        if len(keys) >= 70:
            break
    keys = sorted(keys)
    return keys[63]


EX_RAW_DATA = file_to_string(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
