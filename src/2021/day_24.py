"""Advent of code 2021
--- Day 24: Arithmetic Logic Unit ---
"""

from collections import defaultdict, namedtuple
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok

VG = None  #  the SN validity graph

Instruction = namedtuple(
    "Instruction",
    ["op", "a", "b"],
)


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        arr = tok(line)

        if len(arr) == 3:
            c = arr[2]
            try:
                c = int(c)
            except ValueError:
                pass
            data.append(Instruction(arr[0], arr[1], c))
        else:
            data.append(Instruction(arr[0], arr[1], None))

    return data


def alu(instructions: list, inputs, reg=None) -> dict:
    """Return the registers"""
    if reg is None:
        reg = defaultdict(int)
    else:
        reg = reg.copy()
    input_value = iter(inputs)
    for ins in instructions:
        ins: Instruction
        if ins.op == "inp":
            # print(reg)
            v = next(input_value)
            v = int(v)
            if not 1 <= v <= 9:
                raise ValueError(f"Input too big {v}")
            reg[ins.a] = v
            continue

        b = ins.b
        if isinstance(b, str):
            b = reg[b]

        if ins.op == "add":
            reg[ins.a] += b
            continue

        if ins.op == "mul":
            reg[ins.a] *= b
            continue

        if ins.op == "div":
            if b == 0:
                raise ValueError("ALU: div 0")
            reg[ins.a] = int(reg[ins.a] / b)
            continue

        if ins.op == "mod":
            if b == 0:
                raise ValueError("ALU: mod 0")
            if b < 0:
                raise ValueError(f"ALU: mod -ve, {b}")
            reg[ins.a] %= b
            continue

        if ins.op == "eql":
            reg[ins.a] = 1 if reg[ins.a] == b else 0

    return reg


def max_sn(dg, size=14, z=0):
    """Navigate the graph via the maximum edge"""

    def iterate(u, sn):
        best, d = sorted(dg[u].items(), key=lambda x: x[1], reverse=True)[0]
        nsn = sn + str(d)
        if best[0] == 14:
            return nsn
        return iterate(best, nsn)

    nodes = [u for u in dg if u == (14 - size, z)]
    nodes = sorted(nodes, key=lambda x: x[1], reverse=True)
    return iterate(nodes[0], "")


def min_sn(dg, size=14, z=0):
    """Navigate the graph via the minimum edge"""

    def iterate(u, sn):
        best, d = sorted(dg[u].items(), key=lambda x: x[1])[0]
        nsn = sn + str(d)
        if best[0] == 14:
            return nsn
        return iterate(best, nsn)

    nodes = [u for u in dg if u == (14 - size, z)]
    nodes = sorted(nodes, key=lambda x: x[1])
    return iterate(nodes[0], "")


def starting_z_values(data):
    """What are the possible starting values for z in any phase.
    We will restrict our tests to these source values.
    The result is achieved by iterating through each phase using the
    possible values of the previous one. Plus we also cap the value based on
    what we found from max_z_values() when working backwards.
    Here place 0 is most significant
    """
    mzv = max_z_values(data)
    print(
        "Maximum starting values for z, based on the instances of div z in each phase"
    )
    print(mzv)
    starting_with = []
    cur_z_values = {0}
    for place in range(14):
        cur_z_values = {z for z in cur_z_values if z <= mzv[place]}
        print(f"{place+1}: {len(cur_z_values)} values")
        print(f"ranging: {min(cur_z_values)} - {max(cur_z_values)}")
        starting_with.append(cur_z_values)
        alu_phase = data[18 * place : 18 * (place + 1)]
        new_z_values = set()
        for d in range(1, 10):
            for z in cur_z_values:
                start_reg = defaultdict(int)
                start_reg["z"] = z
                reg = alu(alu_phase, [d], start_reg)
                new_z_values.add(reg["z"])
        cur_z_values = new_z_values
    return starting_with


def max_z_values(data):
    """What are the maximum values for the starting value of z in any phase?
    1st phase = 0 ,....
    last phase = <26 so that the div z 26 takes it to 0
    for place 13 (2nd from last) it will be 26**2 and similar applied where ever
    div z 26 occurs going back.
    Here place is zero based i.e. 0 is the most significant
    """

    # restriction from the left
    mzp_left = [0]
    z_values = {0}
    for place in range(14):
        alu_phase = data[18 * place : 18 * (place + 1)]
        new_z_values = set()
        for d in range(1, 10):
            for z in z_values:
                start_reg = defaultdict(int)
                start_reg["z"] = z
                reg = alu(alu_phase, [d], start_reg)
                new_z_values.add(reg["z"])
        z_values = sorted(new_z_values, reverse=True)[:1]
        mzp_left.append(max(z_values))

    # restriction from the right - for phases where we div z 26
    # we will need to factor up by 26 for the limit o the source
    mzp_right = [None] * 14
    mzp_right[13] = 26
    cur_max = 1
    div_z = [ins.b for ins in data if ins.op == "div" and ins.a == "z"]
    for i, d in enumerate(reversed(div_z)):
        place = 13 - i
        cur_max *= d
        mzp_right[place] = cur_max

    mzp = [min(a, b) for a, b in zip(mzp_left, mzp_right)]

    return mzp


def find_valid_sources(data: list, place: int, targets: set, z_values: set):
    """For a given
    - place 1-14 (1 being the most significant digit)
    - set of desired target values for z once that phase of the ALU has run
    return a dictionary keyed on digit where the value is a
    set of values for z (from, to)
    """
    alu_phase = data[18 * (place - 1) : 18 * place]
    sources = defaultdict(list)
    for z in z_values:
        for d in range(1, 10):
            start_reg = defaultdict(int)
            start_reg["z"] = z
            reg = alu(alu_phase, [d], start_reg)
            if reg["z"] in targets:
                sources[d].append((z, reg["z"]))

    return sources


def build_validity_graph(data: list, initial_targets=None, size=14):
    """Most of the work is creating a directed graph where
    a node is (place, starting z)
    an edge is the digit which will take you to the next place
    Here place is 1..14 where 1 is the most significant digit
    Once we have it then navigating a route for valid numbers
    becomes straight forward
    """
    global VG
    if VG:
        return

    # first build a list of the possible starting values
    # for z in each phase
    phase_starting_values = starting_z_values(data)

    print()
    print("Build graph")

    targets = {0}
    if initial_targets is not None:
        targets = initial_targets

    dg = defaultdict(dict)
    for place in range(14, 14 - size, -1):
        sources = find_valid_sources(
            data, place, targets, phase_starting_values[place - 1]
        )
        targets = set()
        for digit, z_values in sources.items():
            for z_from, z_to in z_values:
                n_from = (place - 1, z_from)
                n_to = (place, z_to)
                dg[n_from][n_to] = digit
                targets.add(z_from)
        print(f"{place} Nodes: {len(dg)}")
    print()

    VG = dg


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    build_validity_graph(data)
    return max_sn(VG)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    build_validity_graph(data)
    return min_sn(VG)


MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(MY_DATA)
solve_part_b(MY_DATA)
