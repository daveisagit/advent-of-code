"""Advent of code 2016
--- Day 13: A Maze of Twisty Little Cubicles ---
"""

from collections import Counter, deque
from operator import add
from common.aoc import file_to_string, aoc_part, get_filename
from common.grid_2d import directions


def parse_data(raw_data):
    """Parse the input"""
    return int(raw_data)


def shortest_path(data, target):
    """as per"""

    def is_space(x, y):
        v = x * x + 3 * x + 2 * x * y + y + y * y
        v += data
        cnt = Counter(f"{v:b}")
        return cnt["1"] % 2 == 0

    bfs = deque()
    bfs.append(((1, 1), 0))
    seen = set()
    while bfs:
        p, steps = bfs.popleft()
        if p in seen:
            continue
        seen.add(p)

        if p == target:
            return steps

        for d in directions.values():
            np = tuple(map(add, p, d))
            x, y = np
            if x >= 0 and y >= 0 and is_space(x, y):
                bfs.append(((np), steps + 1))

    return None


@aoc_part
def solve_part_a(data, target) -> int:
    """Solve part A"""
    sp = shortest_path(data, target)
    return sp


def most_points(data):
    """as per"""

    def is_space(x, y):
        v = x * x + 3 * x + 2 * x * y + y + y * y
        v += data
        cnt = Counter(f"{v:b}")
        return cnt["1"] % 2 == 0

    bfs = deque()
    bfs.append(((1, 1), 0))
    seen = {}
    while bfs:
        p, steps = bfs.popleft()
        if p in seen:
            continue
        seen[p] = steps

        if steps > 50:
            continue

        for d in directions.values():
            np = tuple(map(add, p, d))
            x, y = np
            if x >= 0 and y >= 0 and is_space(x, y):
                bfs.append(((np), steps + 1))

    return sum(1 for s in seen.values() if s <= 50)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    return most_points(data)


EX_RAW_DATA = file_to_string(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)


MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)


solve_part_a(EX_DATA, (7, 4))
solve_part_a(MY_DATA, (31, 39))

solve_part_b(MY_DATA)
