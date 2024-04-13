"""Advent of code 2016
--- Day 21: Scrambled Letters and Hash ---
"""

from itertools import permutations
import re
from common.aoc import file_to_list, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        op = None
        args = None
        if line[:13] == "swap position":
            rr = re.search(r"(swap position) (\d) with position (\d)", line)
            op = rr.group(1)
            args = (int(rr.group(2)), int(rr.group(3)))
        elif line[:11] == "swap letter":
            rr = re.search(r"(swap letter) (.) with letter (.)", line)
            op = rr.group(1)
            args = (rr.group(2), rr.group(3))
        elif line[:12] == "rotate based":
            rr = re.search(r"(rotate based) on position of letter (.)", line)
            op = rr.group(1)
            args = (rr.group(2),)
        elif line[:6] == "rotate":
            rr = re.search(r"(rotate) (right|left) (\d) step", line)
            op = rr.group(1)
            args = (rr.group(2), int(rr.group(3)))
        elif line[:7] == "reverse":
            rr = re.search(r"(reverse) positions (\d) through (\d)", line)
            op = rr.group(1)
            args = (int(rr.group(2)), int(rr.group(3)))
        elif line[:4] == "move":
            rr = re.search(r"(move) position (\d) to position (\d)", line)
            op = rr.group(1)
            args = (int(rr.group(2)), int(rr.group(3)))
        data.append((op, args))

    return data


def scramble(moves, start):
    """Scramble"""
    lst = list(start)
    for op, args in moves:
        # print(op, args, "".join(lst))
        if op == "swap position":
            a, b = args
            lst[a], lst[b] = lst[b], lst[a]
            continue
        if op == "swap letter":
            a, b = args
            ai = lst.index(a)
            bi = lst.index(b)
            lst[ai], lst[bi] = b, a
            continue
        if op == "rotate based":
            a = args[0]
            rs = lst.index(a)
            if rs >= 4:
                rs += 1
            rs += 1
            rs %= len(lst)
            lst = lst[-rs:] + lst[:-rs]
            continue
        if op == "rotate":
            d, rs = args
            rs %= len(lst)
            if d == "right":
                lst = lst[-rs:] + lst[:-rs]
            else:
                lst = lst[rs:] + lst[:rs]
        if op == "reverse":
            a, b = args
            b += 1
            l1 = lst[:a]
            l2 = lst[a:b]
            l3 = lst[b:]
            l2 = list(reversed(l2))
            lst = l1 + l2 + l3
        if op == "move":
            ai, bi = args
            a = lst.pop(ai)
            lst.insert(bi, a)
    return "".join(lst)


@aoc_part
def solve_part_a(data, start="abcde") -> int:
    """Solve part A"""
    s = scramble(data, start)
    return s


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    pwd = "fbgdceah"
    start = "abcdefgh"
    for s in permutations(start, len(start)):
        if scramble(data, s) == pwd:
            return "".join(s)
    return None


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA, start="abcdefgh")

solve_part_b(MY_DATA)
