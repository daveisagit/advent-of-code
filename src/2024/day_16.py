"""Advent of code 2024
--- Day 16: Reindeer Maze ---
"""

from heapq import heappop, heappush
from operator import add


from common.aoc import (
    file_to_list,
    aoc_part,
    get_filename,
)
from common.grid_2d import (
    list_2d_to_dict,
    rotations,
)


def parse_data(raw_data):
    """Parse the input"""
    sz, grid, poi = list_2d_to_dict(
        raw_data, poi_labels="SE", replace_poi_with_char="."
    )
    start = poi["S"]
    target = poi["E"]
    return grid, sz, start, target


def get_best_path_score(data):
    grid, sz, start, target = data
    h = []
    # state = (score, pos, direction)
    state = 0, start, 0
    heappush(h, state)
    seen = set()
    while h:
        score, pos, d = heappop(h)
        if (pos, d) in seen:
            continue
        seen.add((pos, d))

        # check if target reached
        if pos == target:
            return score

        # add options to heap
        dv = rotations[d]
        np = tuple(map(add, pos, dv))

        if pos in grid and grid[pos] == ".":
            state = score + 1, np, d
            heappush(h, state)

        nd = (d + 1) % 4
        state = score + 1000, pos, nd
        heappush(h, state)

        nd = (d - 1) % 4
        state = score + 1000, pos, nd
        heappush(h, state)


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    return get_best_path_score(data)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    # this time keep path in state
    # (score, path, direction)
    # if we match best score then add path to seats
    score_best_path = get_best_path_score(data)
    grid, sz, start, target = data
    h = []
    state = 0, (start,), 0
    heappush(h, state)
    seats = set()
    best_score_at = {}
    while h:
        score, pth, d = heappop(h)
        pos = pth[-1]
        if (pos, d) in best_score_at:
            if score > best_score_at[(pos, d)]:
                continue
        best_score_at[(pos, d)] = score

        if score > score_best_path:
            break

        if pos == target:
            if score == score_best_path:
                seats |= set(pth)
            continue

        # add options to heap
        dv = rotations[d]
        np = tuple(map(add, pos, dv))

        if pos in grid and grid[pos] == ".":
            state = score + 1, pth + (np,), d
            heappush(h, state)

        nd = (d + 1) % 4
        state = score + 1000, pth, nd
        heappush(h, state)

        nd = (d - 1) % 4
        state = score + 1000, pth, nd
        heappush(h, state)

    return len(seats)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
