"""Advent of code 2020
--- Day 14: Docking Data ---
"""

from collections import defaultdict
import json
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        arr = tok(line, "=")
        if arr[0][:4] == "mask":
            data.append(("mask", arr[1]))
            continue
        v = int(arr[1])
        ml = int(arr[0][4:-1])
        data.append(("mem", ml, v))
    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    memory = defaultdict(int)
    or_mask = 0
    and_mask = 0
    for row in data:
        if row[0] == "mask":
            msk: str = row[1]
            or_mask = int(msk.replace("X", "0"), 2)
            and_mask = int(msk.replace("X", "1"), 2)
            continue
        _, loc, val = row
        val = val | or_mask
        val = val & and_mask
        memory[loc] = val

    return sum(memory.values())


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""

    def binary_fixed_length(num, length=8):
        return format(num, "0{}b".format(length))

    memory = defaultdict(int)
    cur_mask = None
    for row in data:
        if row[0] == "mask":
            cur_mask: str = row[1]
            continue

        _, loc, val = row
        loc2 = f"{loc:0b}"
        ll = len(loc2)

        # massage the mask
        mask = cur_mask[-ll:]
        mask = "".join(["X" if b == "X" else max(a, b) for a, b in zip(loc2, mask)])
        mask = cur_mask[:-ll] + mask

        # replace all combinations for X
        x_pos = [p for p, x in enumerate(mask) if x == "X"]
        x_cnt = len(x_pos)
        rng = 2**x_cnt
        for x in range(rng):
            x2 = binary_fixed_length(x, x_cnt)
            m = list(mask)
            for i, p in enumerate(x_pos):
                m[p] = x2[i]
            m = "".join(m)
            l = int(m, 2)
            memory[l] = val

    return sum(memory.values())


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
