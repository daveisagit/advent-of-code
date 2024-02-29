"""Advent of code 2018
--- Day 4: Repose Record ---
"""

from collections import defaultdict
from itertools import pairwise
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    data = []
    guard = None
    gid = None
    raw_data = sorted(raw_data)
    for line in raw_data:
        dt = line[1:17]
        minute = int(dt[-2:])
        if "Guard #" in line:
            prv_gid = gid
            gid = int(tok(line[26:])[0])
            if guard:
                data.append((prv_gid, guard))
            guard = [minute]
        else:
            guard.append(minute)
    data.append((gid, guard))
    return data


def dump_hist(log):
    """Visual"""
    for gid, hist in log:
        hist = "".join(["#" if x else "." for x in hist])
        print(f"{gid:10} {hist}")


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    log = []
    for gid, times in data:
        intervals = pairwise(times)
        sleep_hist = [0] * 60
        for p, (a, b) in enumerate(intervals):
            if p % 2 == 1:
                for i in range(a, b):
                    sleep_hist[i] = 1
        log.append((gid, sleep_hist))

    totals = defaultdict(int)
    for gid, sleep_hist in log:
        totals[gid] += sum(sleep_hist)

    sleepy_guard = sorted(totals.items(), key=lambda x: x[1])[-1][0]
    sleep_pattern = [sleep_hist for gid, sleep_hist in log if gid == sleepy_guard]
    sleep_pattern = list(zip(*sleep_pattern))
    sleep_pattern = [sum(m) for m in sleep_pattern]
    mode = max(sleep_pattern)
    minute = sleep_pattern.index(mode)

    return minute * sleepy_guard


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    log = []
    for gid, times in data:
        intervals = pairwise(times)
        sleep_hist = [0] * 60
        for p, (a, b) in enumerate(intervals):
            if p % 2 == 1:
                for i in range(a, b):
                    sleep_hist[i] = 1
        log.append((gid, sleep_hist))

    gids = {gid for gid, _ in log}
    best = 0
    best_result = None
    for g in gids:
        sleep_pattern = [sleep_hist for gid, sleep_hist in log if gid == g]
        sleep_pattern = list(zip(*sleep_pattern))
        sleep_pattern = [sum(m) for m in sleep_pattern]
        mode = max(sleep_pattern)
        minute = sleep_pattern.index(mode)
        if mode > best:
            best = mode
            best_result = g * minute

    return best_result


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
