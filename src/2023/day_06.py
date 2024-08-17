"""Advent of code 2023
--- Day 6: Wait For It ---
"""

from math import ceil, floor, prod, sqrt
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    rows = []
    for line in raw_data:
        row = [int(x) for x in tok(line[10:]) if x]
        rows.append(row)
    data = tuple((a, b) for a, b in zip(*rows))
    return data


def get_quadratic_roots(a, b, c):
    """Quadratic roots, assuming they will exist"""
    x1 = (-b - sqrt(b**2 - 4 * a * c)) / (2 * a)
    x2 = (-b + sqrt(b**2 - 4 * a * c)) / (2 * a)

    if (b**2 - 4 * a * c) != 0:
        return min(x1, x2), max(x1, x2)
    else:
        return x1, None


def get_ways_to_break_record(race_time: int, record_dist: int) -> int:
    """Return the number of ways to break the record

    T = Race time
    R = Record

    Distance covered if held for x = x(T-x)
    Record is broken if x(T-x) > R

    or
    xT - x^2 - R > 0
    => x^2 - xT + R < 0

    We have a quadratic a=1, b=-T, c=R
    and we want integer solutions for x that lie in between the roots
    """

    b = -race_time
    c = record_dist

    x1, x2 = get_quadratic_roots(1, b, c)

    # a single root means no solution

    if x2 is not None:

        # floor+1 & ceil-1 because roots maybe integers
        # and we want record breakers not equalizers

        # if we did
        # ceil instead of floor+1 and
        # floor instead of ceil-1
        # then that would result in record equalizers being included

        a1 = floor(x1) + 1
        a2 = ceil(x2) - 1
        return a2 - a1 + 1

    return 0


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    return prod(get_ways_to_break_record(t, r) for t, r in data)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    data = [int(v) for v in ["".join(str(x) for x in t) for t in zip(*data)]]
    return get_ways_to_break_record(data[0], data[1])


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
