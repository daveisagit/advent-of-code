"""Advent of code 2019
--- Day 7: Amplification Circuit ---
"""

from itertools import permutations
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    data = [int(i) for i in tok(raw_data[0], ",")]
    return data


def run(data, inputs, address=0):
    """Run it"""

    def get_args(cnt, mode=0):
        args = []
        for arg in data[address + 1 : address + 1 + cnt]:
            am = mode % 10
            mode = mode // 10
            if am == 0:
                args.append(data[arg])
            if am == 1:
                args.append(arg)
        return args

    running = True
    outputs = []
    while running:
        op = data[address]
        pm = op // 100
        op = op % 100

        if op == 99:
            running = False

        # add
        if op == 1:
            sz = 4
            args = get_args(2, pm)
            r = args[0] + args[1]
            c = data[address + 3]
            data[c] = r

        # multiply
        if op == 2:
            sz = 4
            args = get_args(2, pm)
            r = args[0] * args[1]
            c = data[address + 3]
            data[c] = r

        # input
        if op == 3:
            if not inputs:
                break
            sz = 2
            c = data[address + 1]
            i = inputs.pop(0)
            data[c] = i

        # output
        if op == 4:
            sz = 2
            c = data[address + 1]
            outputs.append(data[c])

        # jump if true
        if op == 5:
            sz = 3
            args = get_args(2, pm)
            if args[0] != 0:
                address = args[1]
                continue

        # jump if false
        if op == 6:
            sz = 3
            args = get_args(2, pm)
            if args[0] == 0:
                address = args[1]
                continue

        # less than
        if op == 7:
            sz = 4
            args = get_args(2, pm)
            c = data[address + 3]
            if args[0] < args[1]:
                data[c] = 1
            else:
                data[c] = 0

        # equal
        if op == 8:
            sz = 4
            args = get_args(2, pm)
            c = data[address + 3]
            if args[0] == args[1]:
                data[c] = 1
            else:
                data[c] = 0

        address += sz

    return outputs, running, address


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    max_out = 0
    for cmb in permutations(range(5)):
        out = 0
        for phase in cmb:
            inputs = [phase, out]
            prog = data.copy()
            outputs, _, _ = run(prog, inputs)
            out = outputs[0]
        if out > max_out:
            max_out = out

    return max_out


def parallel_run(data, cmb) -> int:
    """Run the 5 amps together for a the given combo"""
    amp_inputs = []
    addresses = [0] * 5
    amp_states = []
    for i in range(5):
        amp_states.append(data.copy())
        amp_inputs.append([cmb[i]])

    out = 0
    cur_amp = 0
    while True:
        amp_inputs[cur_amp].append(out)
        outputs, running, address = run(
            amp_states[cur_amp], amp_inputs[cur_amp], addresses[cur_amp]
        )
        addresses[cur_amp] = address
        out = outputs[0]
        if not running and cur_amp == 4:
            return out
        cur_amp += 1
        cur_amp %= 5


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    max_out = 0
    for cmb in permutations(range(5, 10)):
        prog = data.copy()
        out = parallel_run(prog, cmb)
        if out > max_out:
            max_out = out

    return max_out


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
