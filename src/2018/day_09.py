"""Advent of code 2018
--- Day 9: Marble Mania ---
"""

from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok
from common.linked_list import Node, insert_after_node, remove_node


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        arr = tok(line)
        players = int(arr[0])
        last = int(arr[6])
        data.append((players, last))
    return data


def get_scores(players, last):
    """Return all the players scores"""
    scores = [0] * players
    c = Node(0)
    c.next = c
    c.prev = c
    for m in range(1, last + 1):
        p = m % players

        if m % 23 == 0:
            scores[p] += m
            for _ in range(7):
                c = c.prev
            scores[p] += c.data
            nc = c.next
            remove_node(c)
            c = nc
            continue

        c1 = c.next
        c = insert_after_node(c1, m)

    return scores


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    for players, last in data:
        scores = get_scores(players, last)
        print(max(scores))
    return len(data)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    players, last = data[0]
    last = last * 100
    scores = get_scores(players, last)
    return max(scores)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(MY_DATA)
