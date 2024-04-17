"""Advent of code 2015
--- Day 14: Reindeer Olympics ---
"""

from collections import defaultdict
import re
from common.aoc import file_to_list, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    deer = {}
    for line in raw_data:
        rr = re.search(
            r"(.+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.",
            line,
        )
        name = rr.group(1)
        attrs = tuple(int(x) for x in rr.groups()[1:])
        deer[name] = attrs
    return deer


def get_travelled(deer, race_duration):
    """How far did they get"""
    travelled = {}
    for n, (speed, duration, rest) in deer.items():
        d = duration + rest
        q, r = divmod(race_duration, d)
        q *= duration
        q += min(r, duration)
        travelled[n] = q * speed
    return travelled


@aoc_part
def solve_part_a(deer, race_duration) -> int:
    """Solve part A"""
    travelled = get_travelled(deer, race_duration)
    return max(travelled.values())


@aoc_part
def solve_part_b(deer, race_duration) -> int:
    """Solve part B"""
    points = defaultdict(int)
    for rd in range(1, race_duration + 1):
        travelled = get_travelled(deer, rd)
        leader_board = sorted(travelled.items(), key=lambda x: x[1], reverse=True)
        leading_dist = leader_board[0][1]
        leaders = {n for n, d in leader_board if d == leading_dist}
        for leader in leaders:
            points[leader] += 1

    return max(points.values())


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA, 1000)
solve_part_a(MY_DATA, 2503)

solve_part_b(EX_DATA, 1000)
solve_part_b(MY_DATA, 2503)
