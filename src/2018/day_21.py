"""Advent of code 2018
--- Day 21: Chronal Conversion ---
"""

from collections import defaultdict
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


def pgm_halts(pgm, bound_reg, registers):
    """Yes but when/why? Dump various things for analysis"""
    states = set()
    ips = defaultdict(int)
    cnt = 0
    prv_3 = 0
    prv_1 = 0
    sol = 0
    while True:
        cnt += 1

        ip = registers[bound_reg]
        ips[ip] += 1

        try:
            ins, args = pgm[ip]
        except IndexError:
            return registers

        # if cnt % 10000 == 0:
        #     dump = f"{cnt:10} {ip:4} {str(registers):50} {ins:6} {args}"
        #     print(dump)

        # if ip in (17, 30) or ip < 7:
        # if 6 <= ip <= 17 or ip == 30:
        #     # tr = tuple(registers)
        #     # if tr in states:
        #     #     return min(st[3] for st in states)
        #     # states.add(tr)
        #     # pass
        #     dump = f"{cnt:10} {ip:4} {str(registers):50} {ins:6} {args}"
        #     print(dump)

        # if ip == 6:
        #     if registers[1] in states:
        #         print(registers[1], "*")
        #     else:
        #         print(registers[1])
        #         states.add(registers[1])

        # if cnt > 100000000:
        #     # for k, v in ips.items():
        #     #     print(k, v)
        #     break

        prv_reg = registers.copy()
        registers = do_op(ins, args, registers)

        dump = f"{cnt:10} {ip:4} {str(prv_reg):50} {ins:6} {str(args):30} {str(registers):50} "

        # if 6 <= ip <= 17 or ip == 30 or prv_reg[1] != registers[1]:
        #     print(dump)

        if ip == 30:
            sol += 1
            print(sol)
            print(dump)
            # print(registers[3])

        # if registers[3] != prv_3:
        #     dump = f"{cnt:10} {ip:4} {str(registers):50} {ins:6} {args}"
        #     print(dump)
        #     prv_3 = registers[3]

        registers[bound_reg] += 1


def next_r3(pgm, bound_reg, registers):
    """Registers 1,3 change value on 17 and 30
    17: R1 is still over 255 ( R1->R1 // 256 ) : resume on 8
    30: R1 is <= 255 and meets the condition for halting : resume on 6
    """
    while True:
        ip = registers[bound_reg]

        try:
            ins, args = pgm[ip]
        except IndexError:
            return registers
        registers = do_op(ins, args, registers)

        if ip in (17, 30):
            return registers

        registers[bound_reg] += 1


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    _, args = data[0]
    bound_reg = args[0]

    registers = [0] * 6
    while True:
        registers = next_r3(data[1:], bound_reg, registers)
        if registers[5] == 17:
            registers[5] = 8
            registers[1] = registers[1] // 256
        else:
            return registers[3]


@aoc_part
def solve_part_b(data) -> int:
    """Solve part A"""
    _, args = data[0]
    bound_reg = args[0]

    registers = [0] * 6
    states = []
    while True:
        registers = next_r3(data[1:], bound_reg, registers)
        if registers[5] == 17:
            registers[5] = 8
            registers[1] = registers[1] // 256
        else:
            if registers[3] in states:
                break
            states.append(registers[3])
            registers[5] = 6
            registers[1] = registers[3]

    return states[-1]


MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(MY_DATA)
solve_part_b(MY_DATA)
