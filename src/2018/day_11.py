"""Advent of code 2018
--- Day 11: Chronal Charge ---
"""

from common.aoc import aoc_part


def parse_data(raw_data):
    """Parse the input"""
    data = raw_data
    return data


def create_grid(sn, sz=300):
    """Create a grid for a given serial number"""
    g = {}
    for x in range(1, sz + 1):
        for y in range(1, sz + 1):
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


def create_sums(g, sz=300, sq=3):
    """Sums for part A"""
    sums = {}
    for x in range(1, sz - sq + 2):
        for y in range(1, sz - sq + 2):
            s = 0
            for xd in range(sq):
                for yd in range(sq):
                    s += g[(x + xd, y + yd)]
            sums[(x, y)] = s
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

    # g = create_grid(18)
    # s = create_sums_b(g)
    # assert s[(90, 269, 16)] == max(s.values())


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    g = create_grid(data)
    sums = create_sums(g)
    ans = sorted(sums.items(), key=lambda x: x[1], reverse=True)[0][0]
    ans = [str(a) for a in ans]
    return ",".join(ans)


def create_sums_b(g, sz=300):
    """Sums for part A"""

    def get_size(sx, sy, ss):
        if ss == 1:
            s = g[(sx, sy)]
        else:
            s = sums[(sx, sy, ss - 1)]
            for b in range(ss - 1):
                s += g[(sx + ss - 1, sy + b)]
                s += g[(sx + b, sy + ss - 1)]
            s += g[(sx + ss - 1, sy + ss - 1)]
        sums[(sx, sy, ss)] = s
        return s

    sums = {}
    for sq in range(1, sz + 1):
        for x in range(1, sz - sq + 2):
            for y in range(1, sz - sq + 2):
                get_size(x, y, sq)
    return sums


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    g = create_grid(data)
    sums = create_sums_b(g)
    ans = sorted(sums.items(), key=lambda x: x[1], reverse=True)[0][0]
    ans = [str(a) for a in ans]
    return ",".join(ans)


run_tests()
solve_part_a(7139)
solve_part_b(7139)
