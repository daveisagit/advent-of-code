"""Advent of code 2019
--- Day 19: Tractor Beam ---
"""

from common.aoc import aoc_part, file_to_string, get_filename
from common.intcode import IntCode


def visualize_beam(beam):
    """Viz"""
    max_x = max(b[0] for b in beam) + 1
    max_y = max(b[1] for b in beam) + 1
    for y in range(0, max_y):
        row = [" "] * (max_x)
        for x in range(0, max_x):
            if (x, y) in beam:
                row[x] = "#"
        print("".join(row))


def get_scan(ic, rng=50):
    """Return points covered by the beam up to the given range"""
    beam = set()
    last_x = 0
    for y in range(rng):
        in_beam = False
        for x in range(last_x, rng):
            o = ic.run([x, y])
            if o[0] == 1:
                if not in_beam:
                    last_x = x
                beam.add((x, y))
                in_beam = True
                continue
            if in_beam:
                break
    return beam


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    ic = IntCode(data)
    beam = get_scan(ic)
    return len(beam)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""

    def in_beam(x, y):
        """is x,y in the beam"""
        if (x, y) in memo_beam:
            return memo_beam[(x, y)]
        o = ic.run([x, y])
        rv = False
        if o[0] == 1:
            rv = True
        memo_beam[(x, y)] = rv
        return rv

    def refine_right_edge(y):
        """Get the max x edge for a y"""
        if y in memo_edge:
            return memo_edge[y]
        # x = y / m1
        x = y * m2[1] // m2[0]
        i = -1
        start_inside = in_beam(x, y)
        if start_inside:
            i = 1
        while True:
            x += i
            if start_inside:
                if not in_beam(x, y):
                    memo_edge[y] = x - i
                    return x - i
            else:
                if in_beam(x, y):
                    memo_edge[y] = x
                    return x

    def estimate_square_gradient():
        """Given the edge gradients m1,m2 estimate the gradient
        for the corner of the square"""
        r1 = m1[0] / m1[1]
        r2 = m2[0] / m2[1]
        m = r2 * ((1 + r1) / (1 + r2))
        return m

    def max_square(y):
        """What's max square for this row being the top of it"""
        if y in memo:
            return memo[y]

        m = estimate_square_gradient()
        x = int(y / m)
        max_x = refine_right_edge(y)
        sq = max_x - x
        i = -1
        start_inside = in_beam(max_x - sq + 1, y + sq - 1)
        if start_inside:
            i = 1
        while True:
            sq += i
            if start_inside:
                if not in_beam(max_x - sq + 1, y + sq - 1):
                    memo[y] = sq - 1
                    return sq - 1
            else:
                if in_beam(max_x - sq + 1, y + sq - 1):
                    memo[y] = sq
                    return sq

    memo_edge = {}
    memo = {}
    memo_beam = {}

    ic = IntCode(data)
    init_range = 50
    beam = get_scan(ic, rng=init_range)
    visualize_beam(beam)
    for y in range(init_range, 0, -1):
        row = {b[0] for b in beam if b[1] == y}
        if row:
            m = max(row)
            if m < init_range - 1:
                break

    m1 = (y, min(row))
    m2 = (y, m)
    sq_at_50 = max_square(50)
    print("Edge gradients: ", m1, m2)
    print(f"Max sq y=50: {max_square(50)}")
    m = estimate_square_gradient()
    print(f"Square gradient: {m:f}")

    y = 100 * 50 // sq_at_50
    print(f"Start: {y}")
    sq_at_y = max_square(y)
    print(f"Max sq y={y}: {sq_at_y}")

    y = 100 * y // sq_at_y
    print(f"Refined: {y}")
    sq_at_y = max_square(y)
    print(f"Max sq y={y}: {sq_at_y}")

    # cant be far now find the closest
    while True:
        if max_square(y) < 100:
            break
        y -= 1
    y += 1

    print(f"Found closest row: {y}")

    x = refine_right_edge(y)
    x -= 99
    return x * 10000 + y


MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))

solve_part_a(MY_RAW_DATA)
solve_part_b(MY_RAW_DATA)
