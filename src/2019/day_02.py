"""Advent of code 2019
--- Day 2: 1202 Program Alarm ---
"""

from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    data = [int(i) for i in tok(raw_data[0], ",")]
    return data


def run(data):
    """Run it"""
    running = True
    step = 0
    while running:
        op = data[step]
        if op == 99:
            running = False
        if op == 1:
            r = data[data[step + 1]] + data[data[step + 2]]
            data[data[step + 3]] = r
        if op == 2:
            r = data[data[step + 1]] * data[data[step + 2]]
            data[data[step + 3]] = r
        step += 4

    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    data_instance = data.copy()
    data_instance[1] = 12
    data_instance[2] = 2
    return run(data_instance)[0]


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    for n in range(100):
        for v in range(100):
            data_instance = data.copy()
            data_instance[1] = n
            data_instance[2] = v
            res = run(data_instance)[0]
            if res == 19690720:
                return 100 * n + v


MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(MY_DATA)
solve_part_b(MY_DATA)
