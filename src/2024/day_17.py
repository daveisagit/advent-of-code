"""Advent of code 2024
--- Day 17: Chronospatial Computer ---
"""

from collections import deque
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data[:3]:
        x = int(line[12:])
        data.append(x)

    arr = tok(raw_data[4][9:], ",")
    d = list(int(g) for g in arr)

    return data, d


# from 2019
class IntCode:
    """The intcode processor"""

    def __init__(self, code) -> None:
        """Store the code in a default dict for unlimited memory"""

        if isinstance(code, list):
            self.code = code
        if isinstance(code, str):
            self.code = [int(i) for i in code.split(",")]

        self.output = []
        self._p = 0
        self._running = False
        self._registers = {}
        self.reset()

    @property
    def is_running(self) -> bool:
        """In case we are pausing for input, check the state"""
        return self._running

    def reset(self):
        """Reset all inputs, outputs, pointers and memory"""
        self._p = 0
        self.output = []
        self._running = True

    def get_val(self, typ, op, arg):
        if typ == "L":
            return arg
        if typ == "C":
            if arg <= 3:
                return arg
            if arg == 4:
                return self._registers["A"]
            if arg == 5:
                return self._registers["B"]
            if arg == 6:
                return self._registers["C"]
            if arg == 7:
                raise RuntimeError("Invalid 7")

    def set_registers(self, a, b, c):
        self._registers["A"] = a
        self._registers["B"] = b
        self._registers["C"] = c

    def do_step(self) -> bool:

        if self._p >= len(self.code):
            self._running = False
            return False

        op = self.code[self._p]

        arg = None
        if self._p + 1 < len(self.code):
            arg = self.code[self._p + 1]

        if op == 0:  # adv
            n = self._registers["A"]
            d = 2 ** self.get_val("C", op, arg)
            res = n // d
            self._registers["A"] = res

        if op == 1:  # bxl
            a = self._registers["B"]
            b = self.get_val("L", op, arg)
            r = a ^ b
            self._registers["B"] = r

        if op == 2:  # bst
            v = self.get_val("C", op, arg)
            r = v % 8
            self._registers["B"] = r

        if op == 3:  # jnz
            v = self._registers["A"]
            if v != 0:
                v = self.get_val("L", op, arg)
                self._p = v
                return False

        if op == 4:  # bxc
            b = self._registers["B"]
            c = self._registers["C"]
            r = b ^ c
            self._registers["B"] = r

        if op == 5:  # out
            v = self.get_val("C", op, arg)
            r = v % 8
            self.output.append(r)

        if op == 6:  # bdv
            n = self._registers["A"]
            d = 2 ** self.get_val("C", op, arg)
            res = n // d
            self._registers["B"] = res

        if op == 7:  # cdv
            n = self._registers["A"]
            d = 2 ** self.get_val("C", op, arg)
            res = n // d
            self._registers["C"] = res

        return True

    def go(self):
        """Run the processor"""
        self._running = True
        while self.is_running:
            if self.do_step():
                self._p += 2

    def once_through(self):
        """Run until we are back at step 0"""
        while self.is_running:
            if self.do_step():
                self._p += 2
            if self._p == 0:
                break

    def get_output(self):
        return ",".join(str(x) for x in self.output)

    def run_for_a_as(self, a):
        self.reset()
        self.set_registers(a, 0, 0)
        self.go()


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    reg, pgm = data
    ic = IntCode(pgm)
    ic._registers["A"] = reg[0]
    ic._registers["B"] = reg[1]
    ic._registers["C"] = reg[2]
    ic.go()
    return ic.get_output()


def analysis(data):

    # On each iteration of the 16 the output will be 0-7
    # (based on whatever a,b,c are at the start of the iteration)

    reg, pgm = data
    ic = IntCode(pgm)

    # Output in Base 8 so remainder 0-7
    # A = quotient|remainder
    # A = Q|r
    print()
    print(f"A = A // 8 on each iteration")
    ic.set_registers(*reg)
    ic._running = True
    q = None
    while ic.is_running:
        print(q, ic._registers)
        a = ic._registers["A"]
        q = a // 8
        ic.once_through()
    print()

    # On the last iteration Q=0, so we need A to
    # be minimum of 8 ** len(pgm)
    min_A = 8 ** len(pgm)
    print(f"Minimum value for A = {min_A}")
    ic.reset()
    ic.set_registers(min_A, 0, 0)
    ic._running = True
    q = None
    while ic.is_running:
        print(ic._registers, ic.output, len(ic.output))
        ic.once_through()
    print()

    # B,C are always reset to something based on A
    # so their values can be ignored at the start of an iteration
    x = (min_A + (min_A * 8)) // 2 + 123456789  # some arbitrary value
    print(f"Arbitrary value for A: {x}")
    print("shows B,C are always reset to something at the start of an iteration")
    ic.run_for_a_as(x)
    out = ic.output

    ic.run_for_a_as(x)
    ic._running = True
    q = None
    while ic.is_running:
        ic._registers["B"] = 0
        ic._registers["C"] = 0
        ic.once_through()
    print(f"Output resetting B/C        : {out}")
    print(f"Output without resetting B/C: {ic.output}")
    print()

    # What values for A give a match
    print(f"Values for A which give an output matching the code {pgm}")
    print(
        "Looking for values of A going backwards that work, matching the end of the list"
    )
    for x in range(8**4):
        ic.run_for_a_as(x)
        sz = len(ic.output)
        if ic.output == pgm[-sz:]:
            q, r = divmod(x, 8)
            print(f"A = {x:<6} {ic.get_output():10} {x:>6} = {q:>5} x 8 + {r}")
    print()

    # for last digit if A=0 we would have quit, so can ignore
    # what works for the previous iteration is A * 8 plus
    # something we don't yet know (value from 0 to 7)

    # !!! SOLUTION !!!
    # We can do a BFS search to find what works
    print("Running a BFS gives a set of values that work")
    answers = []
    bfs = deque()
    # state = A, length of code from the end to match
    state = (0, 1)
    bfs.append(state)
    while bfs:
        state = bfs.popleft()
        x, sz = state
        if sz == len(pgm) + 1:
            answers.append(x)
            continue
        for v in range(8):
            a = x * 8 + v
            ic.run_for_a_as(a)
            if ic.output == pgm[-sz:]:
                new_state = a, sz + 1
                bfs.append(new_state)

    for a in answers:
        ic.run_for_a_as(a)
        assert ic.output == pgm
        print(a, ic.get_output())
    print()

    print(f"Minimum: {min(answers)}")


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    reg, pgm = data
    ic = IntCode(pgm)

    answers = []
    bfs = deque()
    # state = A, length of code from the end to match
    state = (0, 1)
    bfs.append(state)
    while bfs:
        state = bfs.popleft()
        x, sz = state
        if sz == len(pgm) + 1:
            answers.append(x)
            continue
        for v in range(8):
            a = x * 8 + v
            ic.run_for_a_as(a)
            if ic.output == pgm[-sz:]:
                new_state = a, sz + 1
                bfs.append(new_state)

    return min(answers)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

analysis(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
