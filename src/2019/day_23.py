"""Advent of code 2019
--- Day 23: Category Six ---
"""

from common.aoc import aoc_part, file_to_string, get_filename
from common.general import window_over
from common.intcode import IntCode


def boot_up(data, nbr=50):
    """Boot up 50 intcode units"""
    ics = []
    for i in range(nbr):
        ic = IntCode(data)
        ics.append(ic)
        ic.input = [i, -1]
        ic.go()
    return ics


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    ics = boot_up(data)
    while True:
        for ic in ics:
            for m, x, y in window_over(ic.output, 3, 3):
                if m == 255:
                    return y
                to_ic = ics[m]
                to_ic.input.extend([x, y])
            ic.output.clear()

        for ic in ics:
            if not ic.input:
                ic.input = [-1]
            ic.go()


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    ics = boot_up(data)
    ic0 = ics[0]
    nat_packet = []
    last_y = None
    while True:

        idle = True
        for ic in ics:
            for m, x, y in window_over(ic.output, 3, 3):
                idle = False
                if m == 255:
                    nat_packet = [x, y]
                    continue
                to_ic = ics[m]
                to_ic.input.extend([x, y])
            ic.output.clear()

        for ic in ics:
            if ic.input:
                idle = False
            else:
                ic.input = [-1]
            ic.go()

        if idle:
            if not nat_packet:
                print("What, no packet!")
                return None
            if nat_packet[1] == last_y:
                return last_y
            last_y = nat_packet[1]
            ic0.input.extend(nat_packet)


MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))

solve_part_a(MY_RAW_DATA)
solve_part_b(MY_RAW_DATA)
