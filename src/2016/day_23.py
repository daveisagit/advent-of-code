"""Advent of code 2016
--- Day 23: Safe Cracking ---
"""

from collections import defaultdict
from copy import deepcopy
from hashlib import md5
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


def run_pgm_a(pgm, reg):
    """Run the program"""
    p = 0
    c = 0
    while True:
        c += 1

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


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    data = deepcopy(data)
    reg = defaultdict(int)
    reg["a"] = 7
    run_pgm_a(data, reg)
    return reg["a"]


def run_pgm_b(pgm, reg, dump=False):
    """Run the program"""
    p = 0
    c = 0
    cont = 0
    acc0 = False
    acc1 = False
    acc2 = False
    acc3 = False
    while True:
        c += 1
        if cont > 0:
            cont -= 1
        pgm_str = str(pgm).encode()
        h = md5(pgm_str).hexdigest()

        if (
            h == "1d0a3715ac2304ae356d9460cd1365ae"
            and p == 9
            and reg["d"] < 239500800 - 2
            and not acc3
        ):
            acc3 = True
            reg["d"] = 1
            reg["a"] = reg["b"] * (239500800 - reg["d"])
            cont = 100

        if (
            h == "9013f2c20c6f77f04dc30771b8284a2e"
            and p == 9
            and reg["d"] < 79833600 - 2
            and not acc2
        ):
            acc2 = True
            reg["d"] = 1
            reg["a"] = reg["b"] * (79833600 - reg["d"])
            cont = 100

        if (
            h == "bf031459d1c9aff46c536b58bf574f4f"
            and p == 9
            and reg["d"] < 19958400 - 2
            and not acc1
        ):
            acc1 = True
            reg["d"] = 1
            reg["a"] = reg["b"] * (19958400 - reg["d"])
            cont = 100

        if h == "29cd69bc7f30ecae920b1e2b1ad8b112" and p == 16 and not acc0:
            acc0 = True
            reg["a"] = 19958400
            reg["b"] = 4
            reg["c"] = 8
            cont = 100

        if dump and cont:
            print(p, reg, h)

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


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    data = deepcopy(data)
    reg = defaultdict(int)
    reg["a"] = 12
    run_pgm_b(data, reg)
    return reg["a"]


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(MY_DATA)
