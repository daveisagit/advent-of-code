"""The inner workings of the intcode processor"""

from collections import defaultdict


class IntCode:  # pylint: disable=R0902
    """The intcode processor"""

    def __init__(self, code) -> None:
        """Store the code in a default dict for unlimited memory"""

        self.memory = defaultdict(int)
        if isinstance(code, list):
            self.code = code
        if isinstance(code, str):
            self.code = [int(i) for i in code.split(",")]

        self.input = []
        self.output = []

        self._p = 0
        self._arg_types = None
        self._modes = None
        self._jump = None
        self._running = False
        self._op = None
        self.debug = False

        self.reset()

    @property
    def is_running(self) -> bool:
        """In case we are pausing for input, check the state"""
        return self._running

    def reset(self):
        """Reset all inputs, outputs, pointers and memory"""
        self._p = 0
        self._relative_base = 0
        self.input = []
        self.output = []
        self._running = True
        for a, v in enumerate(self.code):
            self.memory[a] = v

    def _get_args(self) -> tuple:

        sz = len(self._arg_types)
        args = []
        mode = self._modes
        for idx, addr in enumerate(range(self._p + 1, self._p + 1 + sz)):

            typ = self._arg_types[idx]
            arg = self.memory[addr]
            am = mode % 10
            mode = mode // 10

            v = arg
            if typ == "I":
                if am == 0:  # position mode
                    v = self.memory[arg]
                if am == 2:  # relative
                    v = self.memory[arg + self._relative_base]
            if typ == "O":
                if am == 2:  # relative
                    v = arg + self._relative_base

            args.append(v)

        if self.debug:
            print(f"{self._op} {args} {self._modes}")

        return tuple(args)

    def run(self, input_values: list | None = None) -> list:
        """Run some input and return the output"""
        if input_values is None:
            input_values = []
        self.reset()
        self.input = input_values
        self.go()
        return self.output

    def go(self):
        """Run the processor"""
        self._running = True
        while self.is_running:

            # reset operation level attributes
            self._arg_types = ""
            self._modes = None
            self._jump = None
            self._op = None

            # get op and modes
            op = self.memory[self._p]
            self._modes = op // 100
            op = op % 100
            self._op = op

            # do the operation and break if pausing for input
            pause = self._do_op(op)
            if pause:
                break

            # jump or next
            if self._jump is None:
                self._p += len(self._arg_types) + 1
            else:
                self._p = self._jump

    def get_memory(self):
        """Get the memory in list form"""
        return [self.memory[a] for a in range(max(self.memory) + 1)]

    def _do_op(self, op) -> bool:

        if op == 99:
            self._running = False

        if op == 1:
            self._add()

        if op == 2:
            self._mlt()

        if op == 3:
            if self._input():
                return False
            return True

        if op == 4:
            self._output()

        if op == 5:
            self._jump_if_true()

        if op == 6:
            self._jump_if_false()

        if op == 7:
            self._less_than()

        if op == 8:
            self._equal()

        if op == 9:
            self._rel_offset()

        return False

    def _add(self):
        """01"""
        self._arg_types = "IIO"
        args = self._get_args()
        a, b, s = args  # pylint: disable=W0632
        r = a + b
        self.memory[s] = r

    def _mlt(self):
        """02"""
        self._arg_types = "IIO"
        args = self._get_args()
        a, b, s = args  # pylint: disable=W0632
        r = a * b
        self.memory[s] = r

    def _input(self):
        """03"""
        self._arg_types = "O"
        if not self.input:
            return False
        args = self._get_args()
        a = args[0]
        v = self.input.pop(0)
        self.memory[a] = v
        return True

    def _output(self):
        """04"""
        self._arg_types = "I"
        args = self._get_args()
        v = args[0]
        self.output.append(v)

    def _jump_if_true(self):
        """05"""
        self._arg_types = "II"
        args = self._get_args()
        cmp, jmp = args  # pylint: disable=W0632
        if cmp != 0:
            self._jump = jmp

    def _jump_if_false(self):
        """06"""
        self._arg_types = "II"
        args = self._get_args()
        cmp, jmp = args  # pylint: disable=W0632
        if cmp == 0:
            self._jump = jmp

    def _less_than(self):
        """07"""
        self._arg_types = "IIO"
        args = self._get_args()
        a, b, s = args  # pylint: disable=W0632
        if a < b:
            self.memory[s] = 1
        else:
            self.memory[s] = 0

    def _equal(self):
        """08"""
        self._arg_types = "IIO"
        args = self._get_args()
        a, b, s = args  # pylint: disable=W0632
        if a == b:
            self.memory[s] = 1
        else:
            self.memory[s] = 0

    def _rel_offset(self):
        """09"""
        self._arg_types = "I"
        args = self._get_args()
        v = args[0]
        self._relative_base += v


def test_day_02_add():
    """Tests from Day 2"""
    ic = IntCode("1,0,0,0,99")
    ic.run()
    assert ic.memory[0] == 2

    ic = IntCode("2,3,0,3,99")
    ic.run()
    assert ic.memory[3] == 6

    ic = IntCode("2,4,4,5,99,0")
    ic.run()
    assert ic.memory[5] == 9801

    ic = IntCode("1,1,1,4,99,5,6,0,99")
    ic.run()
    assert ic.memory[0] == 30


def test_day_05_cmp_jmp():
    """Tests from Day 5"""
    ic = IntCode("3,9,8,9,10,9,4,9,99,-1,8")
    o = ic.run([8])
    assert o[0] == 1
    o = ic.run([7])
    assert o[0] == 0

    ic = IntCode("3,3,1108,-1,8,3,4,3,99")
    o = ic.run([8])
    assert o[0] == 1
    o = ic.run([7])
    assert o[0] == 0

    ic = IntCode("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9")
    o = ic.run([118])
    assert o[0] == 1
    o = ic.run([0])
    assert o[0] == 0

    ic = IntCode("3,3,1105,-1,9,1101,0,0,12,4,12,99,1")
    o = ic.run([118])
    assert o[0] == 1
    o = ic.run([0])
    assert o[0] == 0

    pgm = """3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
        1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
        999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"""
    ic = IntCode(pgm)
    o = ic.run([7])
    assert o[0] == 999
    o = ic.run([8])
    assert o[0] == 1000
    o = ic.run([9])
    assert o[0] == 1001


def test_day_09_rel():
    """Tests from Day 9"""
    pgm = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
    ic = IntCode(pgm)
    o = ic.run()
    assert o == ic.code

    ic = IntCode("1102,34915192,34915192,7,4,7,99,0")
    o = ic.run()
    assert o[0] == 1219070632396864

    ic = IntCode("104,1125899906842624,99")
    o = ic.run()
    assert o[0] == 1125899906842624


def test_all():
    """Run all tests"""
    test_day_02_add()
    test_day_05_cmp_jmp()
    test_day_09_rel()


test_all()
