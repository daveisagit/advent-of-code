"""Advent of code 2018
--- Day 12: Subterranean Sustainability ---
"""

from itertools import pairwise
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import window_over
from common.linear_algebra import poly_from_points, poly_value
from common.numty import search_for_polynomial_sequence


def parse_data(raw_data):
    """Parse the input"""
    state = raw_data[0][15:]
    rules = {}
    for line in raw_data[2:]:
        k = line[:5]
        v = line[9]
        rules[k] = v
    return state, rules


def iterate(state, offset, rules):
    """Return new state"""

    pad = "....."
    for i in range(5):
        if state[i] == "#":
            break
    i = max(5 - i, 0)
    offset += i
    pre = pad[:i]

    for i in range(1, 6):
        if state[-i] == "#":
            break
    i = max(6 - i, 0)
    post = pad[:i]
    state = pre + state + post

    new_state = ""
    for w in window_over(state, 5):
        np = rules.get(w, ".")
        new_state += np
    return new_state, offset - 2


def get_generations(data, n=20):
    state, rules = data
    offset = 0
    generations = []
    for _ in range(200):
        ans = sum(i - offset if c == "#" else 0 for i, c in enumerate(state))
        generations.append(ans)
        state, offset = iterate(state, offset, rules)
    return generations


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    state, rules = data
    offset = 0
    for _ in range(20):
        state, offset = iterate(state, offset, rules)
    ans = sum(i - offset if c == "#" else 0 for i, c in enumerate(state))
    return ans


def analysis(data):
    """Find when things repeat"""
    state, rules = data
    offset = 0
    generations = []
    for _ in range(200):
        ans = sum(i - offset if c == "#" else 0 for i, c in enumerate(state))
        generations.append(ans)
        state, offset = iterate(state, offset, rules)

    x = search_for_polynomial_sequence(generations, l_bound=1, u_bound=150)

    diff = [b - a for a, b in pairwise(generations)]
    i = 0
    for i, w in enumerate(window_over(diff, 5)):
        if min(w) == max(w):
            break
    return i, diff[i], generations[i]


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    start, difference, pot_total = analysis(data)
    g = 50000000000
    xg = g - start
    xt = xg * difference
    ans = pot_total + xt
    return ans


@aoc_part
def solve_part_c(data) -> int:
    """Solve part C"""
    generations = get_generations(data, 200)
    print(f"Part A: {generations[20]}")
    m, start = search_for_polynomial_sequence(generations, l_bound=1, u_bound=10)
    x_points = tuple(range(start, start + m + 1, m))
    y_points = tuple(generations[x] for x in x_points)
    ply = poly_from_points(x_points, y_points)
    return poly_value(ply, 50000000000)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(MY_DATA)
solve_part_c(MY_DATA)
