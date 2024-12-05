"""Advent of code 2024
--- Day 5: Print Queue ---
"""

from common.aoc import (
    file_to_list,
    aoc_part,
    get_filename,
)
from common.general import input_sections, tok


def parse_data(raw_data):
    """Parse the input"""
    rules = set()
    secs = input_sections(raw_data)

    for sec in secs[0]:
        arr = tok(sec, "|")
        arr = tuple(int(x) for x in arr)
        rules.add(arr)

    pages = []
    for sec in secs[1]:
        arr = tok(sec, ",")
        arr = [int(x) for x in arr]
        pages.append(arr)

    return rules, pages


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    rules, pages = data

    sm = 0
    for line in pages:

        ok = True
        for idx, b in enumerate(line):
            for a in line[:idx]:
                # we expect a<b, if there is a rule
                # saying b<a then that's wrong
                test = (b, a)
                if test in rules:
                    ok = False
                    break
            if not ok:
                break

        if ok:
            v = line[(len(line) - 1) // 2]
            sm += v

    return sm


@aoc_part
def solve_part_b(data) -> int:
    """Solve part A"""
    rules, pages = data

    sm = 0
    bad = []
    for line in pages:

        ok = True
        for idx, b in enumerate(line):
            for a in line[:idx]:
                # we expect a<b, if there is a rule
                # saying b<a then that's wrong
                test = (b, a)
                if test in rules:
                    ok = False
                    break
            if not ok:
                break

        if not ok:
            bad.append(line)

    for line in bad:

        # keeping swapping rule failures until there are no more
        # hopefully not an infinite loop??
        ok = False
        while not ok:
            ok = True
            for idx_b, b in enumerate(line):
                for idx_a, a in enumerate(line[:idx_b]):
                    # we expect a<b, if there is a rule
                    # saying b<a then that's wrong
                    test = (b, a)
                    if test in rules:
                        line[idx_a], line[idx_b] = line[idx_b], line[idx_a]
                        ok = False
                        break
                if not ok:
                    break

        v = line[(len(line) - 1) // 2]
        sm += v

    return sm


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
