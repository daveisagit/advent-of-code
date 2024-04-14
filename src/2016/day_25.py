"""Advent of code 2016
--- Day 25: Clock Signal ---
"""

from collections import defaultdict
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        arr = tok(line)
        op = arr[0]
        args = []
        for x in arr[1:]:
            try:
                x = int(x)
            except ValueError:
                pass
            args.append(x)
        row = (op, tuple(args))
        data.append(row)
    return data


def run_pgm(pgm, reg):
    """Run the program"""
    p = 0
    c = 0
    output = []
    while True:
        c += 1
        if len(output) == 20:
            break

        try:
            op, args = pgm[p]
        except IndexError:
            break

        v_args = [reg[a] if isinstance(a, str) else a for a in args]

        if op == "inc":
            reg[args[0]] += 1
            p += 1
            continue

        if op == "dec":
            reg[args[0]] -= 1
            p += 1
            continue

        if op == "cpy":
            reg[args[1]] = v_args[0]
            p += 1
            continue

        if op == "jnz":
            if v_args[0] != 0:
                p += v_args[1]
            else:
                p += 1
            continue

        if op == "tgl":
            q = p + v_args[0]
            if q < len(pgm):
                t_op, t_args = pgm[q]
                if t_op in ("inc", "dec", "tgl"):
                    n_op = "inc"
                    if t_op in ("inc"):
                        n_op = "dec"
                else:
                    n_op = "jnz"
                    if t_op in ("jnz"):
                        n_op = "cpy"
                pgm[q] = (n_op, t_args)

            p += 1
            continue

        if op == "out":
            output.append(str(v_args[0]))
            p += 1
            continue

    return "".join(output)


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    v1 = "01" * 10
    v2 = "10" * 10
    a = 0
    while True:
        reg = defaultdict(int)
        reg["a"] = a
        output = run_pgm(data, reg)
        if output in (v1, v2):
            return a
        a += 1


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    return len(data)


MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(MY_DATA)
