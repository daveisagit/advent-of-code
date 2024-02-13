"""Advent of code 2019
--- Day 13: Care Package ---
"""

from time import sleep
from common.aoc import aoc_part, file_to_string, get_filename
from common.console import print_at
from common.general import window_over
from common.intcode import IntCode


def parse_data(raw_data):
    """Parse the input"""
    data = raw_data
    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    ic = IntCode(data)
    o = ic.run()
    return sum(1 for x, y, t in window_over(o, 3, 3) if t == 2)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""

    def draw_output(o):
        nonlocal score
        x_margin = 3
        char_map = [" ", "#", "X", "-", "o"]
        for x, y, t in window_over(o, 3, 3):
            if x == -1 and y == 0:
                txt = str(t)
                score = t
            else:
                txt = char_map[t]
            print_at(txt, x + x_margin, y)

    for _ in range(60):
        print()

    ic = IntCode(data)
    ic.memory[0] = 2
    ic.input.append(0)
    paddle = None
    score = 0
    while ic.is_running:
        ic.output.clear()
        ic.go()

        if paddle is None:
            paddle = [(x, y) for x, y, t in window_over(ic.output, 3, 3) if t == 3][0][
                0
            ]
        ball = [(x, y) for x, y, t in window_over(ic.output, 3, 3) if t == 4]
        if ball:
            ball = ball[0][0]

        # in case you like to chill out and watch
        if score < 5000:
            sleep(0.005)

        draw_output(ic.output)

        # follow the ball
        if ball:
            joy = 0
            if paddle > ball:
                joy = -1
            if paddle < ball:
                joy = 1
            paddle += joy
            ic.input.append(joy)

    return score


MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))

solve_part_a(MY_RAW_DATA)
solve_part_b(MY_RAW_DATA)
