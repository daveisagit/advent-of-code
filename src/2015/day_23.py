"""Advent of code 2015
--- Day 23: Opening the Turing Lock ---
"""

from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        arr = tok(line, ",")
        arr2 = tok(arr[0])
        op = arr2[0]
        arg = arr2[1]
        jx = None
        if len(arr) > 1:
            jx = int(arr[1])
        if arg not in ("a", "b"):
            arg = int(arg)

        t = (op, arg, jx)
        data.append(t)

    return data


def run_pgm(pgm, registers=None, p=0):
    """Run the program"""
    if registers is None:
        registers = {"a": 0, "b": 0}

    while True:

        try:
            op, arg, jx = pgm[p]
        except IndexError:
            return registers

        # print(p, op, arg, jx, registers)

        if op == "hlf":
            registers[arg] //= 2
            p += 1
            continue

        if op == "tpl":
            registers[arg] *= 3
            p += 1
            continue

        if op == "inc":
            registers[arg] += 1
            p += 1
            continue

        if op == "jmp":
            p += arg
            continue

        if op == "jie":
            if registers[arg] % 2 == 0:
                p += jx
            else:
                p += 1
            continue

        if op == "jio":
            if registers[arg] == 1:
                p += jx
            else:
                p += 1
            continue


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    reg = run_pgm(data)
    return reg["b"]


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    registers = {"a": 1, "b": 0}
    reg = run_pgm(data, registers=registers)
    return reg["b"]


MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(MY_DATA)

solve_part_b(MY_DATA)
