"""Advent of code 2016
--- Day 17: Two Steps Forward ---
"""

from collections import deque
from hashlib import md5
from operator import add
from common.aoc import file_to_string, aoc_part, get_filename
from common.grid_2d import directions_UDLR


def parse_data(raw_data):
    """Parse the input"""
    data = raw_data
    return data


def shortest_path(salt):
    """Return the UDLR path"""
    d_map = ["U", "D", "L", "R"]
    pos = (0, 0)
    bfs = deque()
    bfs.append(("", pos))
    while bfs:
        route, pos = bfs.popleft()
        if pos == (3, 3):
            return route

        s = f"{salt}{route}"
        s = s.encode()
        h = md5(s).hexdigest()

        for d, v in directions_UDLR.items():
            nxt = tuple(map(add, pos, v))
            if not (0 <= nxt[0] <= 3 and 0 <= nxt[1] <= 3):
                continue
            i = d_map.index(d)
            c = h[i]
            if c in "0123456789a":
                continue
            bfs.append((route + d, nxt))

    return None


@aoc_part
def solve_part_a(salt) -> str:
    """Solve part A"""
    return shortest_path(salt)


def longest_path(salt):
    """Return the UDLR path"""
    d_map = ["U", "D", "L", "R"]
    pos = (0, 0)
    bfs = deque()
    bfs.append(("", pos))
    lp = 0
    while bfs:
        route, pos = bfs.popleft()
        if pos == (3, 3):
            lp = max(lp, len(route))
            continue

        s = f"{salt}{route}"
        s = s.encode()
        h = md5(s).hexdigest()

        for d, v in directions_UDLR.items():
            nxt = tuple(map(add, pos, v))
            if not (0 <= nxt[0] <= 3 and 0 <= nxt[1] <= 3):
                continue
            i = d_map.index(d)
            c = h[i]
            if c in "0123456789a":
                continue
            bfs.append((route + d, nxt))

    return lp


@aoc_part
def solve_part_b(salt) -> int:
    """Solve part B"""
    return longest_path(salt)


EX_RAW_DATA = file_to_string(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

assert shortest_path("ihgpwlah") == "DDRRRD"
assert shortest_path("kglvqrro") == "DDUDRLRRUDRD"
assert shortest_path("ulqzkmiv") == "DRURDRUDDLLDLUURRDULRLDUUDDDRR"


solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

assert longest_path("ihgpwlah") == 370
assert longest_path("kglvqrro") == 492
assert longest_path("ulqzkmiv") == 830

solve_part_b(MY_DATA)
