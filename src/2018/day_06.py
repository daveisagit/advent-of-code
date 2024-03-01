"""Advent of code 2018
--- Day 6: Chronal Coordinates ---
"""

from collections import Counter, defaultdict
from operator import sub
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok
from common.grid_2d import get_grid_limits, manhattan


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        arr = tok(line, ",")
        arr = [int(a) for a in arr]
        data.append((arr[1], arr[0]))
    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    min_r, min_c, max_r, max_c = get_grid_limits(data)
    distances = defaultdict(dict)
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            p = (r, c)
            for i, q in enumerate(data):
                d = tuple(map(sub, p, q))
                d = manhattan(d)
                distances[p][i] = d

    nearest = defaultdict(int)
    for p, dd in distances.items():
        c = Counter(dd.values())
        shortest = min(c.keys())
        points = [i for i, d in dd.items() if d == shortest]
        if len(points) > 1:
            nearest[p] = None
        else:
            nearest[p] = points[0]

    infinite = set()
    for r in range(min_r, max_r + 1):
        infinite.add(nearest[(r, 0)])
        infinite.add(nearest[(r, max_c)])
    for c in range(min_c, max_c + 1):
        infinite.add(nearest[(0, c)])
        infinite.add(nearest[(max_r, c)])

    finite = [i for i in nearest.values() if i not in infinite]
    c = Counter(finite)
    ans = c.most_common(1)[0][1]

    return ans


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    min_r, min_c, max_r, max_c = get_grid_limits(data)
    distances = defaultdict(dict)
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            p = (r, c)
            for i, q in enumerate(data):
                d = tuple(map(sub, p, q))
                d = manhattan(d)
                distances[p][i] = d

    cnt = 0
    for p, dd in distances.items():
        if sum(dd.values()) < 10000:
            cnt += 1
    return cnt


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
