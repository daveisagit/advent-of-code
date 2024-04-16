"""Advent of code 2015
--- Day 7: Some Assembly Required ---
"""

from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok

BITS = 65535


def parse_data(raw_data):
    """Parse the input"""
    data = {}
    for line in raw_data:
        arr = tok(line, "->")
        trg = arr[1]
        arr = tok(arr[0])
        op = None
        if len(arr) == 1:
            args = arr
        if len(arr) == 2:
            op = arr[0]
            args = arr[1:]
        if len(arr) == 3:
            op = arr[1]
            args = [arr[0], arr[2]]
        pargs = []
        for x in args:
            try:
                x = int(x)
            except ValueError:
                pass
            pargs.append(x)
        args = tuple(pargs)
        t = op, args
        data[trg] = t

    return data


def resolve(data, values=None):
    """Get all the values"""

    def gv(v):
        if isinstance(v, int):
            return v
        return values.get(v, None)

    if values is None:
        values = {k: None for k in data}
    remain = [k for k, v in values.items() if v is None]
    while remain:
        for trg, (op, args) in data.items():
            if values.get(trg) is not None:
                continue

            if op is None:
                values[trg] = gv(args[0])
                continue

            if op == "NOT":
                v = gv(args[0])
                if v is not None:
                    values[trg] = BITS - v
                continue

            v1 = gv(args[0])
            v2 = gv(args[1])
            if v1 is None or v2 is None:
                continue

            if op == "AND":
                values[trg] = v1 & v2
                continue

            if op == "OR":
                values[trg] = v1 | v2
                continue

            if op == "LSHIFT":
                values[trg] = v1 << v2
                continue

            if op == "RSHIFT":
                values[trg] = v1 >> v2
                continue

        remain = [k for k, v in values.items() if v is None]

    return values


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    values = resolve(data)
    return values.get("a")


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    values = resolve(data)
    b = values.get("a")
    values = {k: None for k in data}
    values["b"] = b
    values = resolve(data, values=values)
    return values.get("a")


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)


solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(MY_DATA)
