"""Advent of code 2016
--- Day 4: Security Through Obscurity ---
"""

from collections import Counter
import re
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        rr = re.search(r"(.+)-(\d+)\[([a-z]{5})\]", line)
        d = (rr.group(1), int(rr.group(2)), rr.group(3))
        data.append(d)
    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    real = 0
    for s, i, cs in data:
        s = s.replace("-", "")
        cnt = Counter(s)
        cs2 = sorted(cnt.items(), key=lambda x: (-x[1], x[0]))
        cs2 = cs2[:5]
        cs2 = [t[0] for t in cs2]
        cs2 = "".join(cs2)
        if cs == cs2:
            real += i
    return real


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    ans = 0
    base = ord("a")
    words = []
    for es, i, cs in data:
        ds = ""
        for c in es:
            if c == "-":
                c = " "
            else:
                c = ord(c) - base + i
                c %= 26
                c += base
                c = chr(c)
            ds += c
        if "northpole" in ds:
            print(i, ds)
            ans = i
        arr = tok(ds)
        words.extend(arr)
    cnt = Counter(words)
    print(cnt)

    return ans


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)


solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(MY_DATA)
