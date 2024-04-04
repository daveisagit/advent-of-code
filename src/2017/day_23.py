"""Advent of code 2017
--- Day 23: Coprocessor Conflagration ---
"""

from collections import defaultdict
from math import ceil, sqrt
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


class CPU:
    """For day 23 coprocessor"""

    def __init__(self, pgm) -> None:
        self.registers = defaultdict(int)
        self.input = []
        self.output = []
        self.p = 0
        self.pgm = pgm
        self.halted = False
        self.waiting = False
        self.send_counter = 0
        self.mul_counter = 0
        self.trace = False
        self.watch_for_changes = {}
        self.dump_at_pointer = []
        self.count = 0
        self.turbo = False
        self.break_after = 0

    def run(self):
        """run"""
        self.waiting = False
        while True:
            self.count += 1

            if self.break_after and self.count > self.break_after:
                break

            save_registers = self.registers.copy()
            try:
                op, args = self.pgm[self.p]
            except IndexError:
                break

            dump = f"{self.p:4}   Op: {op} {str(args):12} Registers: {dict(self.registers)}"

            if self.p in self.dump_at_pointer:
                print(dump)

            if self.trace:
                print(dump)

            if self.turbo:

                # Hurry up e
                if self.p == 16:
                    self.registers["e"] = self.registers["b"] - 1

                # Hurry up d
                if self.p == 20:
                    self.registers["d"] = self.registers["b"] - 1
                    b = self.registers["b"]

                    # careful to set f=0 (as per @14) if b is not prime
                    # which is the gate (@24) for h +1
                    b_prime = True
                    for d in range(2, ceil(sqrt(b))):
                        if b % d == 0:
                            b_prime = False
                            break
                    if not b_prime:
                        self.registers["f"] = 0

            self.do_step()

            if self.watch_for_changes:
                for r in self.watch_for_changes:
                    if save_registers[r] != self.registers[r]:
                        print(dump)

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

        if op == "sub":
            self.registers[r] -= v
            self.p += 1
            return

        if op == "mul":
            self.registers[r] *= v
            self.p += 1
            self.mul_counter += 1
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

        if op == "jnz":
            if a != 0:
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
    cpu = CPU(data)
    cpu.run()
    return cpu.mul_counter


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    cpu = CPU(data)
    cpu.registers["a"] = 1
    # cpu.watch_for_changes = {"f"}
    cpu.turbo = True
    cpu.run()
    return cpu.registers["h"]


MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(MY_DATA)

solve_part_b(MY_DATA)
