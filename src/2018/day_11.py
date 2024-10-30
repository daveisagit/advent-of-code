"""Advent of code 2018
--- Day 11: Chronal Charge ---
"""

from common.aoc import aoc_part

SIZE = 300


def create_grid(sn):
    """Create a grid for a given serial number"""
    g = {}
    for x in range(1, SIZE + 1):
        for y in range(1, SIZE + 1):
            rid = x + 10
            pl = rid * y
            pl += sn
            pl *= rid
            hd = 0
            if pl >= 100:
                hd = int(str(pl)[-3])
            pl = hd - 5
            g[(x, y)] = pl
    return g


def create_cumulative_grid(g):
    """Cumulative from origin"""
    cg = {}
    for x in range(1, SIZE + 1):
        for y in range(1, SIZE + 1):
            a = cg.get((x - 1, y - 1), 0)
            b = cg.get((x - 1, y), 0)
            c = cg.get((x, y - 1), 0)
            cg[(x, y)] = b + c - a + g[(x, y)]
    return cg


def create_sums(g):
    """Sums for part A"""
    cg = create_cumulative_grid(g)
    sums = {}
    for x in range(1, SIZE - 1):
        for y in range(1, SIZE - 1):
            a = cg.get((x - 1, y - 1), 0)
            b = cg.get((x + 2, y - 1), 0)
            c = cg.get((x - 1, y + 2), 0)
            d = cg.get((x + 2, y + 2), 0)
            sums[(x, y)] = d - b - c + a
    return sums


def run_tests():
    """Unit tests"""
    g = create_grid(57)
    assert g[(122, 79)] == -5
    g = create_grid(39)
    assert g[(217, 196)] == 0
    g = create_grid(71)
    assert g[(101, 153)] == 4

    g = create_grid(18)
    s = create_sums(g)
    assert s[(33, 45)] == 29
    assert max(s.values()) == 29
    g = create_grid(42)
    s = create_sums(g)
    assert s[(21, 61)] == 30
    assert max(s.values()) == 30

    g = create_grid(18)
    s = create_sums_b(g)
    assert s[(90, 269, 16)] == max(s.values())


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    g = create_grid(data)
    sums = create_sums(g)
    ans = sorted(sums.items(), key=lambda x: x[1], reverse=True)[0][0]
    ans = [str(a) for a in ans]
    return ",".join(ans)


def create_sums_b(g):
    """Sums for part A"""
    cg = create_cumulative_grid(g)
    sums = {}
    for sq in range(1, SIZE + 1):
        for x in range(1, SIZE - sq + 2):
            for y in range(1, SIZE - sq + 2):
                a = cg.get((x - 1, y - 1), 0)
                b = cg.get((x + sq - 1, y - 1), 0)
                c = cg.get((x - 1, y + sq - 1), 0)
                d = cg.get((x + sq - 1, y + sq - 1), 0)
                sums[(x, y, sq)] = d - b - c + a
    return sums


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    g = create_grid(data)
    sums = create_sums_b(g)
    ans = sorted(sums.items(), key=lambda x: x[1], reverse=True)[0][0]
    ans = [str(a) for a in ans]
    return ",".join(ans)


# run_tests()
solve_part_a(7139)
solve_part_b(7139)
