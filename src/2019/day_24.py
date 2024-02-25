"""Advent of code 2019
--- Day 24: Planet of Discord ---
"""

from operator import add
from common.aoc import file_to_list, aoc_part, get_filename
from common.grid_2d import directions


def parse_data(raw_data):
    """Parse the input"""
    bugs = set()
    for ri, line in enumerate(raw_data):
        for ci, c in enumerate(line):
            if c == "#":
                bugs.add((ri, ci))
    return bugs


def viz_grid(bugs):
    """Visual"""
    for r in range(5):
        row = ""
        for c in range(5):
            p = "."
            if (r, c) in bugs:
                p = "#"
            row += p
        print(row)
    print()


def iterate_a(bugs):
    """Return a new layout"""
    new_layout = set()
    for r in range(5):
        for c in range(5):
            pos = (r, c)
            if (r, c) in bugs:
                cnt = 0
                for d in directions.values():
                    n = tuple(map(add, d, pos))
                    if n in bugs:
                        cnt += 1
                if cnt == 1:
                    new_layout.add(pos)
                continue

            cnt = 0
            for d in directions.values():
                n = tuple(map(add, d, pos))
                if n in bugs:
                    cnt += 1
            if 1 <= cnt <= 2:
                new_layout.add(pos)
    return frozenset(new_layout)


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    bugs = frozenset(data)
    layouts = set()
    while True:
        if bugs in layouts:
            break
        layouts.add(bugs)
        bugs = iterate_a(bugs)

    # viz_grid(bugs)
    ans = 0
    for bug in bugs:
        idx = bug[0] * 5 + bug[1]
        ans += 2**idx

    return ans


def iterate_b(bugs):
    """Return a new layout"""

    def get_adjacent(pos):
        lvl, pos = pos
        for d in directions.values():
            n = tuple(map(add, d, pos))
            r, c = n
            if r == -1:
                yield (lvl + 1, (1, 2))
                continue
            if r == 5:
                yield (lvl + 1, (3, 2))
                continue
            if c == -1:
                yield (lvl + 1, (2, 1))
                continue
            if c == 5:
                yield (lvl + 1, (2, 3))
                continue
            if r == 2 and c == 2:
                r, c = pos
                if r == 1 and c == 2:
                    for c in range(5):
                        yield (lvl - 1, (0, c))
                    continue
                if r == 3 and c == 2:
                    for c in range(5):
                        yield (lvl - 1, (4, c))
                    continue
                if r == 2 and c == 1:
                    for r in range(5):
                        yield (lvl - 1, (r, 0))
                    continue
                if r == 2 and c == 3:
                    for r in range(5):
                        yield (lvl - 1, (r, 4))
                    continue

            yield (lvl, n)

    def for_level(level):
        for r in range(5):
            for c in range(5):
                if r == c == 2:
                    continue
                pos = (level, (r, c))
                if pos in bugs:
                    cnt = 0
                    for n in get_adjacent(pos):
                        if n in bugs:
                            cnt += 1
                    if cnt == 1:
                        new_layout.add(pos)
                    continue
                cnt = 0
                for n in get_adjacent(pos):
                    if n in bugs:
                        cnt += 1
                if 1 <= cnt <= 2:
                    new_layout.add(pos)

    new_layout = set()
    min_level = min(p[0] for p in bugs)
    max_level = max(p[0] for p in bugs)
    for l in range(min_level - 1, max_level + 2):
        for_level(l)
    return frozenset(new_layout)


@aoc_part
def solve_part_b(data, iterations=10) -> int:
    """Solve part B"""
    bugs = frozenset({(0, p) for p in data})
    for _ in range(iterations):
        bugs = iterate_b(bugs)

    # uncomment for testing

    # min_level = min(p[0] for p in bugs)
    # max_level = max(p[0] for p in bugs)
    # print(min_level, max_level)
    # for l in reversed(range(min_level, max_level + 1)):
    #     bugs_on_level = {p[1] for p in bugs if p[0] == l}
    #     print(f"Level: {-l}")
    #     viz_grid(bugs_on_level)

    return len(bugs)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA, iterations=200)
