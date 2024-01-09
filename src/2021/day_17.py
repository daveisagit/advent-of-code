"""Advent of code 2021
--- Day 17: Trick Shot ---
"""

import math
from common.aoc import file_to_string, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    arr = raw_data.split(",")
    x_values = arr[0]
    y_values = arr[1]

    arr = x_values.split("=")
    min_x = int(arr[1].split("..")[0])
    max_x = int(arr[1].split("..")[1])

    arr = y_values.split("=")
    min_y = int(arr[1].split("..")[0])
    max_y = int(arr[1].split("..")[1])

    data = min_x, max_x, min_y, max_y
    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A - its a Tn number to hit the lowest row in the target area"""
    _, _, min_y, _ = data
    y_depth = abs(min_y)
    return y_depth * (y_depth - 1) // 2


def inv_tri(tn):
    """Returns a float approximating the nth triangle number"""
    return (math.sqrt(1 + 8 * tn) - 1) / 2


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    min_px, max_px, min_py, max_py = data

    min_vx = int(math.ceil(inv_tri(min_px)))
    max_vx = max_px
    print("Vx range: ", min_vx, max_vx)

    y_depth = abs(min_py)
    min_vy = min_py
    max_vy = y_depth * (y_depth - 1) // 2  # part A
    print("Vy range", min_vy, max_vy)

    cnt = 0
    for vy in range(min_vy, max_vy + 1):
        for vx in range(min_vx, max_vx + 1):
            t = 0
            if vy > 0:
                t = 2 * vy + 1  # need to have returned to ground zero
            while True:
                px = vx * (vx + 1) // 2
                if t < vx:
                    px -= (vx - t) * ((vx - t) + 1) // 2  # T(vx) - T(t)

                # print(vx, t, px)
                if px > max_px:
                    break

                py = t * (2 * vy + 1 - t) / 2
                if py < min_py:
                    break

                if min_px <= px <= max_px and min_py <= py <= max_py:
                    cnt += 1
                    break

                t += 1

    return cnt


EX_RAW_DATA = file_to_string(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
