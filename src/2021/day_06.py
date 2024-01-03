"""Advent of code 2021
--- Day 6: Lanternfish ---
"""

from itertools import pairwise
from common.aoc import file_to_string, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    data = tok(raw_data, delim=",")
    data = [int(n) for n in data]
    return data


def new_day(fishes):
    """Return the new day state"""
    zeros = sum(1 if f == 0 else 0 for f in fishes)
    new_fishes = [8] * zeros
    cur_fishes = [(f - 1) % 7 if f < 8 else 7 for f in fishes]
    return cur_fishes + new_fishes


def after_n_days(fishes, n):
    """State after n days"""
    for _ in range(n):
        fishes = new_day(fishes)
    return len(fishes)


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    return after_n_days(data, 80)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    days = []
    fishes = data
    for _ in range(90):
        days.append(len(fishes))
        fishes = new_day(fishes)

    dow = 256 % 7  # the day of the week the 256 sample will be done
    week_num = 256 // 7  # the week in which day 256 occurs
    weekly_sample = days[dow::7]

    print("Weekly sample", weekly_sample)

    diff = weekly_sample
    sample_set = set(weekly_sample)
    diff_orders = [weekly_sample]
    while True:
        diff = [b - a for a, b in pairwise(diff)]
        diff_orders.append(diff)

        # once the most recent values are repeated we can stop
        # if the last 4 are found in the weekly then we have found
        # where the fibonacci pattern
        recent_set = set(diff[-4:])
        chk = recent_set.difference(sample_set)
        if not chk:
            break

    print("Difference Orders")
    for o, diff in enumerate(diff_orders):
        print(o, diff)

    while len(weekly_sample) <= week_num:
        last = diff_orders[-1][-1]
        last_idx = diff_orders[0].index(last)
        n = diff_orders[0][last_idx + 1]
        diff_orders[-1].append(n)

        for o in range(len(diff_orders) - 2, -1, -1):
            d = diff_orders[o + 1][-1]
            n = diff_orders[o][-1] + d
            diff_orders[o].append(n)

    return diff_orders[0][-1]


EX_RAW_DATA = file_to_string(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
