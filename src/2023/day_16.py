"""Advent of code 2023
--- Day 16: The Floor Will Be Lava ---
"""

from collections import deque
from operator import add
from common.aoc import file_to_list, aoc_part, get_filename
from common.grid_2d import grid_lists_to_dict, directions


def parse_data(raw_data):
    """Parse the input"""
    data = raw_data
    size = len(raw_data)
    floor = grid_lists_to_dict(raw_data, content_filter="/\-|")
    return size, floor


# assume >^<v for current direction ordering when mapping
actors = {
    "\\": ["v", "<", "^", ">"],
    "/": ["^", ">", "v", "<"],
    "-": [">", "<>", "<", "<>"],
    "|": ["^v", "^", "^v", "v"],
}


def get_energised_tiles(size, floor, pos=(0, -1), d=">"):
    """Play out all possible paths to get the energised set of tiles"""
    bfs = deque()
    state = pos, d
    bfs.append(state)
    seen = set()
    energised = set()
    while bfs:
        state = bfs.popleft()
        if state in seen:
            continue
        seen.add(state)
        pos, d = state

        dv = directions[d]
        np = tuple(map(add, pos, dv))

        # off grid
        if not (0 <= np[0] < size and 0 <= np[1] < size):
            continue

        energised.add(np)

        # carry on
        if np not in floor:
            bfs.append((np, d))
            continue

        # next direction(s)
        di = list(directions).index(d)
        actor = floor[np]
        for nd in list(actors[actor][di]):
            bfs.append((np, nd))

    return energised


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    size, floor = data
    energised = get_energised_tiles(size, floor)
    return len(energised)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    size, floor = data
    best = 0
    for d in directions:
        for i in range(size):
            if d == "v":
                starting_position = (-1, i)
            elif d == "^":
                starting_position = (size, i)
            elif d == ">":
                starting_position = (i, -1)
            else:
                starting_position = (i, size)
            energised = get_energised_tiles(size, floor, pos=starting_position, d=d)
            best = max(best, len(energised))

    return best


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
