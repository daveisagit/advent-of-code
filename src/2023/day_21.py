"""Advent of code 2023
--- Day 21: Step Counter ---
"""

from collections import Counter, deque
from operator import add
from common.aoc import file_to_list, aoc_part, get_filename
from common.grid_2d import directions
from common.linear_algebra import poly_from_points, poly_value
from common.numty import extend_polynomial_sequence, search_for_polynomial_sequence


def parse_data(raw_data):
    """Parse the input"""
    pots = set()
    size = len(raw_data)
    for ri, row in enumerate(raw_data):
        for ci, content in enumerate(row):
            p = (ri, ci)
            if content == "S":
                start = p
                continue
            if content == "#":
                pots.add(p)
    return start, pots, size


def get_plots(start, size, pots, step_limit=50):
    """Return a dict of plots keyed on position where the value is
    the first step it is encountered"""

    bfs = deque()
    state = start, 0
    bfs.append(state)
    plots = {}
    while bfs:
        state = bfs.popleft()
        p, s = state

        if p in plots:
            continue

        cc_p = tuple(x % size for x in p)
        if cc_p in pots:
            continue
        else:
            plots[p] = s

        if s == step_limit:
            continue

        for d in directions.values():
            np = tuple(map(add, p, d))
            new_state = np, s + 1
            bfs.append(new_state)

    return plots


@aoc_part
def solve_part_a(data, steps=6) -> int:
    """Solve part A"""
    start, pots, size = data
    plots = get_plots(start, size, pots, step_limit=steps)
    parity = steps % 2
    # its everywhere we've visited that matches the odd/even parity
    # for the number of steps
    plots = {p: d for p, d in plots.items() if d % 2 == parity}
    return len(plots)


@aoc_part
def solve_part_b(data, steps=5000, sample_size=500) -> int:
    """Solve part B
    Need to find a repeating pattern over some congruence class
    The pattern is likely to be a quadratic sequence as we are increasing over an area.
    The layout flips between an odd and even parity
    """
    start, pots, size = data

    plot_distances = get_plots(start, size, pots, step_limit=sample_size)
    parity = steps % 2
    plots = {p: d for p, d in plot_distances.items() if d % 2 == parity}

    # create some data to analyse
    # we want a sequence for the number of plots we can finish on
    # after n steps
    cnt = Counter(plots.values())
    seq = [
        sum(c for d, c in cnt.items() if d <= s and d % 2 == parity)
        for s in range(sample_size)
    ]

    # look for a quadratic sequence over some congruence class
    m, first_term = search_for_polynomial_sequence(seq, size, size**2, deg=2)
    offset = steps % m
    print(f"steps={steps} repeat={m} offset={offset}")

    # quotient is the number of leaps of m
    # to get to answer for the total steps required
    q = steps // m

    # extract the congruence class matching our required case
    offset_seq = seq[offset::m]

    # remove the first terms as they have not settled into a pattern yet
    offset_seq = offset_seq[first_term:]
    q -= first_term

    # extend the sequence
    offset_seq = extend_polynomial_sequence(offset_seq, forward=q, backward=0)
    return offset_seq[q]


@aoc_part
def solve_part_b_x(data) -> int:
    """Another way, clue in the question steps, 26501365 = 65 + 202300 x 131
    All plots are reachable within their manhattan distance from the start
    After 65 steps we get the full manhattan diamond inside the single starting grid
    This repeats after another 131 steps, creating 8 more diamonds (9 in total)
    After another 131 steps, a further layer giving 25 diamonds
    If we know the amount of plots after steps 65, 196 and 327
    We can create a quadratic function from these 3 points
    """
    steps = 26501365
    start, pots, size = data

    n = steps - size // 2
    assert n % size == 0
    x = tuple(x * size + size // 2 for x in range(3))
    plot_distances = get_plots(start, size, pots, step_limit=x[2])
    y = tuple(
        len({p for p, d in plot_distances.items() if d <= s and d % 2 == s % 2})
        for s in x
    )
    print(f"x={x} y={y}")
    poly = poly_from_points(x, y, expect_integer=False)
    return poly_value(poly, steps)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA, steps=64)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA, steps=26501365, sample_size=2000)

solve_part_b_x(MY_DATA)
