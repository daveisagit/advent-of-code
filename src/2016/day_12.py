"""Advent of code 2016
--- Day 12: Leonardo's Monorail ---
"""

from collections import defaultdict
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        arr = tok(line)
        op = arr[0]
        args = []
        for x in arr[1:]:
            try:
                x = int(x)
            except ValueError:
                pass
            args.append(x)
        row = (op, tuple(args))
        data.append(row)
    return data


def run_pgm(pgm, reg):
    """Run the program"""
    p = 0
    while True:
        try:
            op, args = pgm[p]
        except IndexError:
            break

        v_args = [reg[a] if isinstance(a, str) else a for a in args]

        if op == "inc":
            reg[args[0]] += 1
            p += 1
            continue

        if op == "dec":
            reg[args[0]] -= 1
            p += 1
            continue

        if op == "cpy":
            reg[args[1]] = v_args[0]
            p += 1
            continue

        if op == "jnz":
            if v_args[0] != 0:
                p += v_args[1]
            else:
                p += 1
            continue


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    reg = defaultdict(int)
    run_pgm(data, reg)
    return reg["a"]


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    reg = defaultdict(int)
    reg["c"] = 1
    run_pgm(data, reg)
    return reg["a"]


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(MY_DATA)
