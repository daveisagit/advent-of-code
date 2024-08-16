"""Advent of code 2022
--- Day 16: Proboscidea Volcanium ---
"""

from collections import defaultdict
import functools
from itertools import product
import re
import sys
from common.aoc import aoc_part, file_to_string, get_filename

sys.setrecursionlimit(5000)


def parse_data(raw_data):
    """Parse the input"""
    r = r"Valve (\w+) .*=(\d*); .* valves? (.*)"
    V, F, D = set(), dict(), defaultdict(lambda: 1000)
    for v, f, us in re.findall(r, raw_data):
        V.add(v)  # store node
        if f != "0":
            F[v] = int(f)  # store flow
        for u in us.split(", "):
            D[u, v] = 1  # store dist

    for k, i, j in product(V, V, V):  # floyd-warshall
        D[i, j] = min(D[i, j], D[i, k] + D[k, j])

    return D, F


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    D, F = data

    @functools.cache
    def search(t, u="AA", vs=frozenset(F)):
        return max(
            [
                F[v] * (t - D[u, v] - 1) + search(t - D[u, v] - 1, v, vs - {v})
                for v in vs
                if D[u, v] < t
            ],
            default=0,
        )

    return search(30)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    D, F = data

    @functools.cache
    def search(t, u="AA", vs=frozenset(F), e=False):
        return max(
            [
                F[v] * (t - D[u, v] - 1) + search(t - D[u, v] - 1, v, vs - {v}, e)
                for v in vs
                if D[u, v] < t
            ]
            + [search(26, vs=vs) if e else 0]
        )

    return search(26, e=True)


EX_RAW_DATA = file_to_string(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
