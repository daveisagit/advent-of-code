"""Advent of code 2016
--- Day 19: An Elephant Named Joseph ---
"""

from math import log
from common.aoc import file_to_string, aoc_part, get_filename
from common.linked_list import Node, insert_after_node, remove_node


def make_list(sz):
    """Parse the input"""
    n = Node((1, 1))
    sn = n
    n.next = n
    n.prev = n
    for i in range(2, sz + 1):
        n = insert_after_node(n, (i, 1))
    return sn


def play(start_with: Node):
    """Play away"""
    n = start_with
    while n.next != n:
        _, amt = n.next.data
        num = n.data[0]
        amt = n.data[1] + amt
        n.data = (num, amt)
        remove_node(n.next)
        n = n.next
    return n


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    sz = int(data)
    ll = make_list(sz)
    n = play(ll)
    return n.data[0]


def play_b(sz):
    """Play away"""
    elves = [(i, 1) for i in range(1, sz + 1)]
    ci = 0
    while len(elves) > 1:
        sz = len(elves)
        ci %= sz
        ti = ci + sz // 2
        ti %= sz

        eid, amt = elves[ci]
        amt += elves[ti][1]
        elves[ci] = (eid, amt)
        elves.pop(ti)
        if ti > ci:
            ci += 1

    return elves[0][0]


def calc_remaining_elf(sz):
    """Log based pattern"""
    e = int(log(sz, 3))
    g = 3**e
    if sz == g:
        c = g
    elif sz < g * 2:
        c = sz - g
    else:
        c = (sz - 2 * g) * 2 + g
    return c


def analysis():
    """Find the pattern"""
    for i in range(5, 1000):
        n = play_b(i)
        c = calc_remaining_elf(i)
        if n != c:
            print(i, n, c)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    sz = int(data)
    return calc_remaining_elf(sz)


EX_RAW_DATA = file_to_string(get_filename(__file__, "ex"))
EX_DATA = EX_RAW_DATA

MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = MY_RAW_DATA

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

# analysis()
solve_part_b(MY_DATA)
