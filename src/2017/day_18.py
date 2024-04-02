"""Advent of code 2017
--- Day 18: Duet ---
"""

from collections import defaultdict
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


class CPU:
    """so we can duet"""

    def __init__(self, pgm, pid) -> None:
        self.registers = defaultdict(int)
        self.registers["p"] = pid
        self.input = []
        self.output = []
        self.p = 0
        self.pgm = pgm
        self.halted = False
        self.waiting = False
        self.send_counter = 0

    def run(self):
        """run"""
        self.waiting = False
        while True:
            self.do_step()
            if self.waiting or self.halted:
                break

    def do_step(self):
        """Process step"""
        try:
            op, args = self.pgm[self.p]
        except IndexError:
            self.halted = True
            return

        r = args[0]
        a = r
        if isinstance(args[0], str):
            a = self.registers[args[0]]

        if op == "snd":
            self.output.append(a)
            self.p += 1
            self.send_counter += 1
            return

        if op == "rcv":
            if self.input:
                v = self.input.pop(0)
                self.registers[r] = v
                self.p += 1
                return
            self.waiting = True
            return

        v = args[1]
        if isinstance(args[1], str):
            v = self.registers[args[1]]

        if op == "set":
            self.registers[r] = v
            self.p += 1
            return

        if op == "add":
            self.registers[r] += v
            self.p += 1
            return

        if op == "mul":
            self.registers[r] *= v
            self.p += 1
            return

        if op == "mod":
            self.registers[r] %= v
            self.p += 1
            return

        if op == "jgz":
            if a > 0:
                self.p += v
            else:
                self.p += 1
            return


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        arr = tok(line)
        args = arr[1:]
        args = [a if a.isalpha() else int(a) for a in args]
        d = (arr[0], args)
        data.append(d)
    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    registers = defaultdict(int)
    stk = []
    lr = None
    p = 0
    cnt = 0
    while True:
        cnt += 1
        try:
            op, args = data[p]
        except IndexError:
            break

        r = args[0]

        if op == "snd":
            stk.append(registers[r])
            p += 1
            continue
        if op == "rcv":
            if registers[r] != 0:
                lr = stk.pop()
                return lr
            p += 1
            continue

        v = args[1]
        if isinstance(args[1], str):
            v = registers[args[1]]

        if op == "set":
            registers[r] = v
            p += 1
            continue

        if op == "add":
            registers[r] += v
            p += 1
            continue

        if op == "mul":
            registers[r] *= v
            p += 1
            continue

        if op == "mod":
            registers[r] %= v
            p += 1
            continue

        if op == "jgz":
            if registers[r] > 0:
                p += v
            else:
                p += 1
            continue

    return lr


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    ca = CPU(data, 0)
    cb = CPU(data, 1)

    while True:

        if not ca.halted:
            ca.run()
            cb.input.extend(ca.output)
            ca.output.clear()

        if not cb.halted:
            cb.run()
            ca.input.extend(cb.output)
            cb.output.clear()

        if not (ca.input and not ca.halted or cb.input and not cb.halted):
            break

    return cb.send_counter


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

BEX_RAW_DATA = file_to_list(get_filename(__file__, "bx"))
BEX_DATA = parse_data(BEX_RAW_DATA)


solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(BEX_DATA)
solve_part_b(MY_DATA)
