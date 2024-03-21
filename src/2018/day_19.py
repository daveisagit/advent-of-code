"""Advent of code 2018
--- Day 19: Go With The Flow ---
"""

from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    pgm = []
    for line in raw_data:
        arr = tok(line)
        args = [int(x) for x in arr[1:]]
        pgm.append((arr[0], args))
    return pgm


def do_op(op, args, registers):
    """Return after state - copied from day 16"""
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


def run_pgm_a(pgm, bound_reg):
    """Run the program"""
    registers = [0] * 6

    while True:

        ip = registers[bound_reg]

        try:
            ins, args = pgm[ip]
        except IndexError:
            break

        registers = do_op(ins, args, registers)

        registers[bound_reg] += 1

    return registers


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    _, args = data[0]
    bound_reg = args[0]
    registers = run_pgm_a(data[1:], bound_reg)
    if bound_reg == 0:
        registers[0] -= 1
    print(registers)
    return registers[0]


def run_pgm_b(
    pgm,
    bound_reg,
    registers=None,
    dump_next=0,
    dump_on_reg_change=None,
    show_history=False,
    dump_limit=None,
):
    """Run the program with plenty of options for analysis"""
    if registers is None:
        registers = [0] * 6
    prv_reg_val = 0
    if show_history:
        history = [None] * show_history

    dn = dump_next
    dc = 0
    while True:

        ip = registers[bound_reg]

        try:
            ins, args = pgm[ip]
        except IndexError:
            break

        if dump_limit and dc > dump_limit:
            break

        dump = f"{ip:4} {str(registers):50} {ins:6} {args}"

        if show_history:
            history.append(dump)
            history.pop(0)

        if dn:
            print(dump)
            dc += 1
            dn -= 1

        if dump_on_reg_change is not None:
            if registers[dump_on_reg_change] != prv_reg_val:
                prv_reg_val = registers[dump_on_reg_change]
                if show_history:
                    print(f"Previous {len(history)}")
                    for h in history:
                        print(h)
                    print("End of history")
                else:
                    print(dump)
                    dc += 1
                dn = dump_next

        registers = do_op(ins, args, registers)

        registers[bound_reg] += 1

    return registers


def run_pgm_c(pgm, bound_reg, registers):
    """Run the program for a set of registers and quit if register 0 changes
    return None if it does not"""

    r0 = registers[0]

    for _ in range(100):

        ip = registers[bound_reg]

        try:
            ins, args = pgm[ip]
        except IndexError:
            return registers

        dump = f"{ip:4} {str(registers):50} {ins:6} {args}"

        if registers[0] != r0:
            return registers
        print(dump)

        registers = do_op(ins, args, registers)

        registers[bound_reg] += 1

    return None


def analysis(data):
    """What the heck is going on"""

    _, args = data[0]
    bound_reg = args[0]

    # Whats going on
    # run_pgm_b(data[1:], bound_reg, registers=[1,0,0,0,0,0], dump_from_start=100)
    # Register 5 increases

    # How does reg 5 change
    # run_pgm_b(data[1:], bound_reg, registers=[1,0,0,0,0,0], dump_on_reg_change=5)
    # Seems to increase amd settle at 10551355

    # Whats going on when we hit it
    # registers = [1, 0, 34, 0, 10550400, 10551355]
    # run_pgm_b(data[1:], bound_reg, registers=registers, dump_from_start=25)
    # around here reg 0 is set to 0 (the original mode)
    # and reg 3 appears to increase by 1

    # Just looking at reg 3 changes
    # registers = [1, 0, 34, 0, 10550400, 10551355]
    # run_pgm_b(data[1:], bound_reg, registers=registers, dump_on_reg_change=3)
    # just keeps going up

    # Just looking at reg 4 changes
    # registers = [1, 0, 34, 0, 10550400, 10551355]
    # run_pgm_b(data[1:], bound_reg, registers=registers, dump_on_reg_change=4)
    # flip flops from 0 to an incremented value

    # Just looking at reg 4 changes close to reg 5
    # registers = [0, 1, 5, 10551350, 0, 10551355]
    # run_pgm_b(
    #     data[1:],
    #     bound_reg,
    #     registers=registers,
    #     dump_on_reg_change=4,
    #     dump_next=10,
    #     dump_limit=200,
    # )
    # r4 = r1 x r3
    # r4 is compared to r5
    # r1 in incremented

    # registers = [1, 2, 5, 10551353, 0, 10551355]
    # run_pgm_b(
    #     data[1:],
    #     bound_reg,
    #     registers=registers,
    #     dump_on_reg_change=4,
    #     show_history=10,
    #     dump_next=10,
    #     dump_limit=50,
    # )

    # r3 is reset to 1 on ip=3, our default entry point

    # Just looking at reg 0 changes
    # registers = [1, 0, 34, 0, 10550400, 10551355]
    # run_pgm_b(data[1:], bound_reg, registers=registers, dump_on_reg_change=0)
    # went from 1 to 6 when r1 x r3 = r5

    # close = (10551355 // 5) - 1
    # registers = [1, 5, 3, close, 0, 10551355]
    # run_pgm_b(
    #     data[1:],
    #     bound_reg,
    #     registers=registers,
    #     dump_on_reg_change=4,
    #     # show_history=10,
    #     dump_next=10,
    #     dump_limit=100,
    # )

    # r0 is updated when r1 x r3 = r5
    # use a new run_pgm_c which quits when r0 changes
    r0 = 0
    for x in range(1, 10551356):
        if 10551355 % x != 0:
            continue
        q = 10551355 // x
        registers = run_pgm_c(data[1:], bound_reg, [r0, x, 3, q, 0, 10551355])
        if registers:
            r0 = registers[0]
            print(registers)
            if registers[bound_reg] >= len(data):
                break


def find_r5(pgm, bound_reg):
    """Run the program for a set of registers and quit if register 0 changed"""

    registers = [0] * 6
    registers[0] = 1
    r0 = 1

    while True:
        ip = registers[bound_reg]

        try:
            ins, args = pgm[ip]
        except IndexError:
            return registers

        if registers[0] != r0:
            return registers[5]

        registers = do_op(ins, args, registers)

        registers[bound_reg] += 1


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    _, args = data[0]
    bound_reg = args[0]

    r5 = find_r5(data[1:], bound_reg)
    sf = 0
    for x in range(1, r5 + 1):
        if r5 % x != 0:
            continue
        sf += x

    # We think r0 is the sum of the factors of r5
    # see if the program halts putting r3 to sf-1
    registers = run_pgm_b(
        data[1:],
        bound_reg,
        registers=[sf, r5, 3, sf - 1, 1, r5],
    )
    print(registers)
    return registers[0]


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

analysis(MY_DATA)
solve_part_b(MY_DATA)
