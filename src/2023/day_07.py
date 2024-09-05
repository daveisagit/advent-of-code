"""Advent of code 2023
--- Day 7: Camel Cards ---
"""

from collections import Counter
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok

ORDER_A = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
ORDER_B = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        arr = tok(line)
        data.append((arr[0], int(arr[1])))
    return data


def second_order_value(hand, order):
    """Equivalent to base 13 the rightmost 5 digits"""
    b = len(order)
    val = 0
    for i, c in enumerate(hand):
        p = 4 - i
        v = b - order.index(c)
        v = (b**p) * v
        val += v
    return val


def hand_type(hand):
    """Return hand type value as
    6: 5 of a kind
    5: 4 of a kind
    4: Full house
    3: 3 of a kind
    2: 2 pair
    1: 1 pair
    0: High card
    """
    c = Counter(hand)
    typ = 0
    if len(c) == 1:
        typ = 6
    if len(c) == 2:
        typ = 5
        if min(c.values()) == 2:
            typ = 4
    if len(c) == 3:
        typ = 3
        if max(c.values()) == 2:
            typ = 2
    if len(c) == 4:
        typ = 1
    return typ


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    ranked = sorted(
        [
            (
                hand_type(hand),
                second_order_value(hand, ORDER_A),
                bid,
            )
            for hand, bid in data
        ]
    )
    return sum((i + 1) * bid for i, (_, _, bid) in enumerate(ranked))


def swap_jokers(hand: str):
    """Return the hand how it would look after swapping jokers for the best option
    We just need to find the most popular card excluding jokers, that will be the
    best card to mimic.
    """
    h = hand.replace("J", "")
    best_card = "A"
    if h:
        cnt = Counter(h)
        cnt = sorted(cnt.items(), key=lambda x: x[1], reverse=True)
        best_card = cnt[0][0]

    h = hand.replace("J", best_card)
    return h


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    ranked = sorted(
        [
            (
                hand_type(swap_jokers(hand)),
                second_order_value(hand, ORDER_B),
                bid,
            )
            for hand, bid in data
        ]
    )
    return sum((i + 1) * bid for i, (_, _, bid) in enumerate(ranked))


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
