"""Advent of code 2023
--- Day 23: A Long Walk ---
"""

from collections import deque
from heapq import heappop, heappush
from common.aoc import file_to_list, aoc_part, get_filename
from common.grid_2d import (
    get_grid_limits,
    grid_lists_to_dict,
    maze_to_graph,
)


def parse_data(raw_data):
    """Parse the input"""
    locations = grid_lists_to_dict(raw_data, content_filter=".<>v^")
    _, _, max_r, _ = get_grid_limits(locations)

    start = list(p for p in locations if p[0] == 0)
    assert len(start) == 1
    start = start[0]

    finish = list(p for p in locations if p[0] == max_r)
    assert len(finish) == 1
    finish = finish[0]

    return start, finish, locations


def get_longest_path_bfs(start, finish, gph):
    """Return the longest path length between start and finish that visits nodes
    only once (not all nodes need to be visited)
    Method: BFS over deque"""
    bfs = deque()
    state = (start,), 0
    bfs.append(state)
    lr = 0
    while bfs:
        path, distance = bfs.popleft()
        cur = path[-1]

        if cur == finish:
            lr = max(lr, distance)
            continue

        for nxt, dst in gph[cur].items():
            if nxt in path:
                continue
            new_path = path + (nxt,)
            bfs.append((new_path, distance + dst))

    return lr


def get_longest_path_heap(start, finish, gph):
    """Return the longest path length between start and finish that visits nodes
    only once (not all nodes need to be visited)
    Method: BFS over heap"""
    h = []
    state = 0, (start,)
    heappush(h, state)
    lr = 0
    while h:
        state = heappop(h)
        travelled, path = state
        travelled = -travelled

        cur = path[-1]

        if cur == finish:
            lr = max(lr, travelled)
            continue

        for nxt, dst in gph[cur].items():
            if nxt in path:
                continue
            new_path = path + (nxt,)
            new_state = -(travelled + dst), new_path
            heappush(h, new_state)

    return lr


def get_longest_path_recursion(start, finish, gph):
    """Return the longest path length between start and finish that visits nodes
    only once (not all nodes need to be visited)"""

    def longest(cur, dst, best):
        if cur == finish:
            return dst
        if cur in seen:
            return best
        # it is more efficient to keep a mutable set maintained
        # rather than passing a new frozen one in the arguments
        seen.add(cur)
        best = max(longest(nxt, d + dst, best) for nxt, d in gph[cur].items())
        seen.remove(cur)
        return best

    seen = set()

    return longest(start, 0, 0)


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    start, finish, locations = data
    gph = maze_to_graph(start, locations, directed=True)
    return get_longest_path_recursion(start, finish, gph)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    start, finish, locations = data
    gph = maze_to_graph(start, locations, path_char="^v<>.")
    return get_longest_path_recursion(start, finish, gph)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
