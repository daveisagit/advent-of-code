"""Advent of code 2020
--- Day 8: Handheld Halting ---
"""

from collections import namedtuple
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok

Instruction = namedtuple("Instruction", ("op", "v"))


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        arr = tok(line)
        data.append(Instruction(arr[0], int(arr[1])))

    return data


def run_the_data(data):
    """Return the acc and True if halted naturally"""
    seen = set()
    idx = 0
    acc = 0
    naturally = False
    while True:
        if idx in seen:
            break
        try:
            ins: Instruction = data[idx]
        except IndexError:
            return 0, False

        seen.add(idx)
        if ins.op == "acc":
            acc += ins.v
            idx += 1

        if ins.op == "jmp":
            idx += ins.v

        if ins.op == "nop":
            idx += 1

        if idx == len(data):
            naturally = True
            break

    return acc, naturally


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    acc, _ = run_the_data(data)
    return acc


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    for step, ins in enumerate(data):
        ins: Instruction
        if ins.op == "acc":
            continue

        data_copy = data.copy()
        if ins.op == "nop":
            data_copy[step] = Instruction("jmp", ins.v)
        else:
            data_copy[step] = Instruction("nop", ins.v)
        acc, halted = run_the_data(data_copy)
        if halted:
            return acc

    return None


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)


solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
