"""Advent of code 2022
--- Day 20: Grove Positioning System ---
"""

from common.aoc import file_to_list, aoc_part, get_filename
from common.linked_list import (
    Node,
    find_node,
    insert_after_node,
    remove_node,
)


def parse_data(raw_data):
    """Parse the input"""
    value_list = [int(x) for x in raw_data]
    n = Node(0)
    start_node = n
    n.next = n
    n.prev = n
    for x in range(1, len(value_list)):
        n = insert_after_node(n, x)

    return value_list, start_node


def decrypt(value_list: list, start_node: Node):

    n = start_node
    m = len(value_list) - 1

    for i, v in enumerate(value_list):

        if v == 0:
            continue

        n = find_node(n, i)

        forward = True
        cnt = abs(v) - 1
        t = n.next
        if v < 0:
            t = n.prev
            forward = False
            cnt += 1

        remove_node(n)

        cnt %= m

        for _ in range(cnt):
            if forward:
                t = t.next
            else:
                t = t.prev

        n = insert_after_node(t, i)

    return n


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    value_list, start_node = data
    n = decrypt(value_list, start_node)
    zero = find_node(n, value_list.index(0))

    n: Node = zero
    lst = []
    while True:
        lst.append(value_list[n.data])
        n = n.next
        if n == zero:
            break

    res = 0
    for i in range(1000, 3001, 1000):
        i %= len(value_list)
        res += lst[i]

    return res


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    KEY = 811589153
    value_list, start_node = data
    value_list = [v * KEY for v in value_list]

    n = start_node
    for _ in range(10):
        n = decrypt(value_list, n)

    zero = find_node(n, value_list.index(0))

    n: Node = zero
    lst = []
    while True:
        lst.append(value_list[n.data])
        n = n.next
        if n == zero:
            break

    res = 0
    for i in range(1000, 3001, 1000):
        i %= len(value_list)
        res += lst[i]

    return res


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

# easiest way to reset the linked list is to re parse the input

EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
