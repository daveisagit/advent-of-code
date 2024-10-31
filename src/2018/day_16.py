"""Advent of code 2018
--- Day 16: Chronal Classification ---
"""

from collections import defaultdict
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok, window_over
from common.logic import exact_cover, mapping_options, resolve_injective_mappings


def parse_data(raw_data):
    """Parse the input"""
    data = []
    pr = 0
    for r, case in enumerate(window_over(raw_data, 4, 4)):
        if not case[0].startswith("Before"):
            pr = r
            break
        before = [int(x) for x in tok(case[0][9:19], ",")]
        op = [int(x) for x in tok(case[1])]
        after = [int(x) for x in tok(case[2][9:19], ",")]
        data.append((before, (op[0], op[1:]), after))

    pgm = []
    for line in raw_data[4 * pr + 2 :]:
        op = [int(x) for x in tok(line)]
        pgm.append(op)

    return data, pgm


def do_op(op, args, registers):
    """Return after state"""
    after = registers.copy()

    if op == "addr":
        a = registers[args[0]]
        b = registers[args[1]]
        c = args[2]
        after[c] = a + b

    if op == "addi":
        a = registers[args[0]]
        b = args[1]
        c = args[2]
        after[c] = a + b

    if op == "mulr":
        a = registers[args[0]]
        b = registers[args[1]]
        c = args[2]
        after[c] = a * b

    if op == "muli":
        a = registers[args[0]]
        b = args[1]
        c = args[2]
        after[c] = a * b

    if op == "banr":
        a = registers[args[0]]
        b = registers[args[1]]
        c = args[2]
        after[c] = a & b

    if op == "bani":
        a = registers[args[0]]
        b = args[1]
        c = args[2]
        after[c] = a & b

    if op == "borr":
        a = registers[args[0]]
        b = registers[args[1]]
        c = args[2]
        after[c] = a | b

    if op == "bori":
        a = registers[args[0]]
        b = args[1]
        c = args[2]
        after[c] = a | b

    if op == "setr":
        a = registers[args[0]]
        c = args[2]
        after[c] = a

    if op == "seti":
        a = args[0]
        c = args[2]
        after[c] = a

    if op == "gtir":
        a = args[0]
        b = registers[args[1]]
        c = args[2]
        after[c] = 1 if a > b else 0

    if op == "gtri":
        a = registers[args[0]]
        b = args[1]
        c = args[2]
        after[c] = 1 if a > b else 0

    if op == "gtrr":
        a = registers[args[0]]
        b = registers[args[1]]
        c = args[2]
        after[c] = 1 if a > b else 0

    if op == "eqir":
        a = args[0]
        b = registers[args[1]]
        c = args[2]
        after[c] = 1 if a == b else 0

    if op == "eqri":
        a = registers[args[0]]
        b = args[1]
        c = args[2]
        after[c] = 1 if a == b else 0

    if op == "eqrr":
        a = registers[args[0]]
        b = registers[args[1]]
        c = args[2]
        after[c] = 1 if a == b else 0

    return after


ops = {
    "addr",
    "addi",
    "mulr",
    "muli",
    "banr",
    "bani",
    "borr",
    "bori",
    "setr",
    "seti",
    "gtir",
    "gtri",
    "gtrr",
    "eqir",
    "eqri",
    "eqrr",
}


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    data, _ = data
    opcodes = defaultdict(set)
    total = 0
    for b, (o, args), a in data:
        cnt = 0
        for op in ops:
            ca = do_op(op, args, b)
            if ca == a:
                opcodes[o].add(op)
                cnt += 1
        if cnt >= 3:
            total += 1

    return total


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    data, pgm = data
    opcodes = defaultdict(set)
    for b, (o, args), a in data:
        for op in ops:
            ca = do_op(op, args, b)
            if ca == a:
                opcodes[o].add(op)
    resolved, op_map = resolve_injective_mappings(opcodes)
    if not resolved:
        print("No can do")
        return None

    registers = [0] * 4
    for e in pgm:
        op = op_map[e[0]]
        args = e[1:]
        registers = do_op(op, args, registers)

    return registers[0]


@aoc_part
def solve_part_c(data) -> int:
    """Solve part B"""
    data, pgm = data
    possibilities = {}

    # Build the Constraints (X)
    # every op and every index accounted for
    constraints = [("#", n) for n in range(len(ops))] + [("o", op) for op in ops]

    for b, (o, args), a in data:
        for op in ops:
            ca = do_op(op, args, b)
            if ca == a:
                # each possibility meets name constraint and an index constraint
                possibilities[(o, op)] = [("#", o), ("o", op)]

    solutions = list(exact_cover(constraints, possibilities))
    if len(solutions) != 1:
        print(f"No unique solution, number of solutions found: {len(solutions)}")
        return None

    solution = solutions[0]

    op_map = {idx: op for idx, op in solution}

    registers = [0] * 4
    for e in pgm:
        op = op_map[e[0]]
        args = e[1:]
        registers = do_op(op, args, registers)

    return registers[0]


@aoc_part
def solve_part_d(data) -> int:
    """Solve part B"""
    data, pgm = data
    opcodes = defaultdict(set)
    for b, (o, args), a in data:
        for op in ops:
            ca = do_op(op, args, b)
            if ca == a:
                opcodes[o].add(op)
    options = list(mapping_options(opcodes))
    if len(options) != 1:
        print("No can do")
        return None

    op_map = options[0]

    registers = [0] * 4
    for e in pgm:
        op = op_map[e[0]]
        args = e[1:]
        registers = do_op(op, args, registers)

    return registers[0]


MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(MY_DATA)

solve_part_b(MY_DATA)

solve_part_c(MY_DATA)

solve_part_d(MY_DATA)
