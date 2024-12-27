"""Advent of code 2024
--- Day 24: Crossed Wires ---
"""

from collections import deque
from functools import lru_cache
import re
from random import randrange
from math import inf

from common.aoc import file_to_list, aoc_part, get_filename
from common.general import input_sections


def parse_data(raw_data):
    """Parse the input"""
    initial = {}
    for line in input_sections(raw_data)[0]:
        sr = re.search(r"(...):\s(\d)", line)
        initial[sr.group(1)] = int(sr.group(2))

    gate_data = []
    for line in input_sections(raw_data)[1]:
        # tqq OR ctb -> qsv
        sr = re.search(r"(...)\s(OR|XOR|AND)\s(...)\s\->\s(...)", line)
        d = tuple(x for x in sr.groups())
        gate_data.append(d)

    return initial, gate_data


class Gate:

    def __init__(self, id, typ, a, b, out):
        self.id = id
        self.typ = typ
        self.a = a
        self.b = b
        self.out = out


def get_gates_wires(data):
    gates = []
    wires = set()
    for id, (a, gt, b, o) in enumerate(data):
        wires.add(a)
        wires.add(b)
        wires.add(o)
        g = Gate(id, gt, a, b, o)
        gates.append(g)
    return gates, wires


def get_gate_outputting_to_wire(gates, w, swaps=()):
    """Which gate is outputting to wire w"""
    rep = {}
    for s in swaps:
        a, b = s
        rep[a] = b
        rep[b] = a
    w = rep.get(w, w)
    gs = [g for g in gates if g.out == w]
    assert len(gs) == 1
    return gs[0]


def run_circuit(initial, gates, outputs, swaps=()):
    """Run the circuit and return a dict for z values"""

    def get_wire_value(w, wires_visited):
        if w in wires_visited:
            raise RecursionError
        wires_visited = frozenset(wires_visited | {w})
        if w in initial:
            return initial[w]
        g = get_gate_outputting_to_wire(gates, w, swaps=swaps)
        if g.typ == "OR":
            return get_wire_value(g.a, wires_visited) | get_wire_value(
                g.b, wires_visited
            )
        if g.typ == "AND":
            return get_wire_value(g.a, wires_visited) & get_wire_value(
                g.b, wires_visited
            )
        if g.typ == "XOR":
            return get_wire_value(g.a, wires_visited) ^ get_wire_value(
                g.b, wires_visited
            )

    out_val = {}
    for o in outputs:
        bit = int(o[1:])
        out_val[bit] = get_wire_value(o, frozenset())

    return out_val


def value_to_dict(v, sz=45):
    """Decimal to dict of binary values"""
    d = {i: 0 for i in range(sz)}
    idx = 0
    while v:
        d[idx] = v % 2
        v = v // 2
        idx += 1
    return d


def value_of_dict(d):
    """dict of binary values to decimal"""
    t = 0
    for idx, v in d.items():
        t += v * (2**idx)
    return t


def dict_to_tuple(d):
    t = ()
    for i in range(len(d)):
        t += (d[i],)
    return t


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    initial, gate_data = data
    gates, wires = get_gates_wires(gate_data)
    outputs = [x for x in wires if x[0] == "z"]
    d = run_circuit(initial, gates, outputs)
    return value_of_dict(d)


def get_contributing_wires(initial, gates, w, swaps=()):
    """All the wires that contribute to the value of w"""
    wires = {w}
    if w in initial:
        return wires
    g = get_gate_outputting_to_wire(gates, w, swaps=swaps)
    if g.a not in wires:
        wires |= get_contributing_wires(initial, gates, g.a, swaps=swaps)
    if g.b not in wires:
        wires |= get_contributing_wires(initial, gates, g.b, swaps=swaps)
    return wires


def get_wrong_bit(exp_d, d):
    """Return the lowest bit for when things went wrong"""
    for idx in range(len(exp_d)):
        if exp_d[idx] != d[idx]:
            return idx
    return None


def test_circuit_old_version(test_bed, gates, outputs, expect, swaps=()):
    """Run over all the tests and return the lowest bit
    number that we have a consistent result for"""
    lowest = inf
    for init, rd in test_bed:
        d = run_circuit(init, gates, outputs, swaps=swaps)
        wb = get_wrong_bit(rd, d)
        if wb is not None:
            lowest = min(lowest, wb)
        if lowest <= expect:
            return lowest

    if lowest == inf:
        lowest = None
    return lowest


def test_circuit(test_bed, gates, outputs, expect, swaps=()):
    """Run over all the tests and return the lowest bit
    number that we have a consistent result for"""

    @lru_cache(maxsize=None)
    def get_wire_value(x, y, w, swaps):
        if w[0] == "x":
            p = int(w[1:])
            return (x >> p) & 1
        if w[0] == "y":
            p = int(w[1:])
            return (y >> p) & 1
        g = get_gate_outputting_to_wire(gates, w, swaps=swaps)
        if g.typ == "AND":
            return get_wire_value(x, y, g.a, swaps) & get_wire_value(x, y, g.b, swaps)
        if g.typ == "OR":
            return get_wire_value(x, y, g.a, swaps) | get_wire_value(x, y, g.b, swaps)
        if g.typ == "XOR":
            return get_wire_value(x, y, g.a, swaps) ^ get_wire_value(x, y, g.b, swaps)

    lowest = inf
    for x, y, rd in test_bed:
        d = {int(w[1:]): get_wire_value(x, y, w, swaps) for w in outputs}
        wb = get_wrong_bit(rd, d)
        if wb is not None:
            lowest = min(lowest, wb)
        if lowest <= expect:
            return lowest

    if lowest == inf:
        lowest = None
    return lowest


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""

    initial, gate_data = data
    gates, wires = get_gates_wires(gate_data)
    gate_outputs = {o for _, _, _, o in gate_data}
    outputs = [x for x in wires if x[0] == "z"]

    # create some tests since the 1 initial state is not enough testing
    # tweak the size of 20 as required, going lower can be worse in that more
    # bad circuits are let through for checking in the later stages
    # up to 50 will run in a couple of mins.
    # several runs of 20 produced a fairly optimal result
    test_bed = []
    for _ in range(20):
        x = randrange(2**44)
        y = randrange(2**44)
        r = x + y
        rd = value_to_dict(r)
        test_bed.append((x, y, rd))

    # start at this bit
    # first_bit_in_error = test_circuit(test_bed, gates, outputs, 0, swaps=())
    first_bit_in_error = test_circuit(test_bed, gates, outputs, 0, swaps=())

    # in case our test bed does not rule out all bad wirings we
    # ought to check out all the avenues
    bfs = deque()
    # state = bit, swaps-initially none
    state = first_bit_in_error, ()
    bfs.append(state)
    seen = set()
    progress = 0
    while bfs:
        state = bfs.popleft()
        bit, swaps = state
        if swaps in seen:
            continue
        seen.add(swaps)

        if bit > progress:
            progress = bit
            print()
            print(f"Bit: {bit:02}")

        swapped_wires = {x for pair in swaps for x in pair}

        # deps are the outputs that could be causing the trouble
        # for this bit position
        zid = f"z{bit:02}"
        deps_this_bit = get_contributing_wires(initial, gates, zid, swaps=swaps)
        deps_lower_bits = set()
        for x in range(bit):
            zid = f"z{x:02}"
            deps_lower_bits |= get_contributing_wires(initial, gates, zid, swaps=swaps)

        # a - we want to pick a wire that affects this bit excluding ones which affect lower bits
        # b - we want to pick any other wire except those that affect the lower bits
        set_a = deps_this_bit - deps_lower_bits
        set_b = gate_outputs - deps_lower_bits
        to_check = len(set_a) * len(set_b)
        print(
            f"Will check {len(set_a)}x{len(set_b)}={to_check} combinations for {swaps}"
        )

        cnt = 0
        for a in set_a:
            for b in set_b:
                cnt += 1
                if a == b:
                    continue
                if a in swapped_wires or b in swapped_wires:
                    continue

                if cnt % 100 == 0:
                    print(f"{cnt} of {to_check}")

                this_swap = tuple(sorted([a, b]))
                new_swaps = tuple(sorted(swaps + (this_swap,)))

                try:
                    # the proposed swap may cause
                    # RecursionError if the circuit has a loop
                    # AssertionError if a wire is assigned to multiple gates outputs
                    wb = test_circuit(test_bed, gates, outputs, bit, swaps=new_swaps)
                    if wb is None:
                        print()
                        print("Found one!")
                        print(
                            ",".join((sorted([x for pair in new_swaps for x in pair])))
                        )
                        print()

                    if len(new_swaps) < 4 and wb > bit:
                        new_state = wb, new_swaps
                        bfs.append(new_state)

                except (AssertionError, RecursionError):
                    continue


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(MY_DATA)
