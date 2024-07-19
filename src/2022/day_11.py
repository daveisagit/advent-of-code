"""Advent of code 2022
--- Day 11: Monkey in the Middle ---
"""

from collections import namedtuple
from math import prod
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok, window_over

Monkey = namedtuple(
    "Monkey",
    (
        "items",
        "operation",
        "test",
        "true",
        "false",
    ),
)


def parse_data(raw_data):
    """Parse the input"""
    monkeys = []
    for data in window_over(raw_data, 6, 7):
        si = tok(data[1], ":")[1]
        si = [int(x) for x in tok(si, ",")]

        op = tok(data[2], "=")[1]
        div = int(tok(data[3], "by")[1])
        tm = int(tok(data[4])[-1])
        fm = int(tok(data[5])[-1])
        monkey_data = Monkey(tuple(si), op, div, tm, fm)
        monkeys.append(monkey_data)

    return monkeys


def do_round(data, holdings, inspection_count, modulo, calming_factor=3):
    for idx, monkey in enumerate(data):
        inspection_count[idx] += len(holdings[idx])
        for lvl in holdings[idx]:
            lvl = eval(monkey.operation, {}, {"old": lvl})
            lvl = lvl // calming_factor
            lvl %= modulo
            if lvl % monkey.test == 0:
                holdings[monkey.true].append(lvl)
            else:
                holdings[monkey.false].append(lvl)
        holdings[idx].clear()


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    modulo = prod(x.test for x in data)
    holdings = [list(m.items) for m in data]
    inspection_count = [0] * len(data)
    for _ in range(20):
        do_round(data, holdings, inspection_count, modulo)
    return prod(sorted(inspection_count, reverse=True)[:2])


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    modulo = prod(x.test for x in data)
    holdings = [list(m.items) for m in data]
    inspection_count = [0] * len(data)
    for _ in range(10000):
        do_round(data, holdings, inspection_count, modulo, calming_factor=1)
    return prod(sorted(inspection_count, reverse=True)[:2])


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
