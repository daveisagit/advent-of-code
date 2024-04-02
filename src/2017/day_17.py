"""Advent of code 2017
--- Day 17: Spinlock ---
"""

from common.aoc import aoc_part, file_to_string, get_filename
from common.linked_list import Node, insert_after_node


def parse_data(raw_data):
    """Parse the input"""
    return int(raw_data)


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    n = Node(0)
    n.next = n
    n.prev = n
    for i in range(1, 2018):
        for _ in range(data):
            n = n.next
        n = insert_after_node(n, i)
    return n.next.data


def dump_list(sn, cn):
    """Visual"""
    n = sn
    s = []
    while True:
        c = str(n.data)
        if n == cn:
            c = "(" + c + ")"
        s.append(c)
        n = n.next
        if n == sn:
            break
    print(" ".join(s))


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    l = 1
    cp = 0
    after_zero = 0
    while True:

        cp += data
        cp %= l
        cp += 1
        l += 1

        if cp == 1:
            after_zero = l - 1

        if l > 50000000:
            return after_zero


EX_RAW_DATA = file_to_string(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(MY_DATA)
