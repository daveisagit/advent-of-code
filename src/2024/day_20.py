"""Advent of code 2024
--- Day 20: Race Condition ---
"""

from collections import Counter
from common.aoc import file_to_list, aoc_part, get_filename
from common.graph import dijkstra
from common.grid_2d import (
    list_2d_to_dict,
    make_graph_from_grid,
    manhattan,
    points_within_manhattan_distance,
)


def parse_data(raw_data):
    """Parse the input"""
    return list_2d_to_dict(raw_data, poi_labels="SE", replace_poi_with_char=".")


def get_savings(data, cheat_duration=2) -> list:
    """Return a list of savings

    Each entry in the list represent the saving for
    a unique pairing (a,b) of 2 points that are valid path points
    where their distance is within the cheat duration.

    A: all path points and their distance from Start
    B: all path points and their distance from End

    We consider all paths points for a in A and
    any b such that manhattan distance of a,b <= cheat duration

    We've assumed that a cheat path can go through where
    any walls might not have been, i.e. all spots on the cheat
    path are valid anyway.
    """
    sz, grid, poi = data
    start = poi["S"]
    end = poi["E"]
    gph = make_graph_from_grid(grid)
    td = dijkstra(gph, start, end)
    dst_start = dijkstra(gph, start, None)
    dst_end = dijkstra(gph, end, None)
    cheats = []
    for a, da in dst_start.items():
        for b in points_within_manhattan_distance(a, cheat_duration):
            if b not in grid:
                continue
            if b not in dst_end:
                continue
            db = dst_end[b]
            cd = manhattan(a, b)
            d = da + cd + db
            if d < td:
                cheats.append(d)

    savings = [td - d for d in cheats]
    return savings


@aoc_part
def solve_part_a(data, save_limit=0, print_detail=True) -> int:
    """Solve part A"""
    saves = get_savings(data, cheat_duration=2)
    saves = [s for s in saves if s >= save_limit]

    if print_detail:
        cnt = Counter(saves)
        cnt = sorted(cnt.items(), key=lambda x: x[0])
        for sv, c in cnt:
            print(c, sv)

    return len(saves)


@aoc_part
def solve_part_b(data, save_limit=50, print_detail=True) -> int:
    """Solve part A"""
    saves = get_savings(data, cheat_duration=20)
    saves = [s for s in saves if s >= save_limit]

    if print_detail:
        cnt = Counter(saves)
        cnt = sorted(cnt.items(), key=lambda x: x[0])
        for sv, c in cnt:
            print(c, sv)

    return len(saves)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)


solve_part_a(EX_DATA)
solve_part_a(MY_DATA, save_limit=100, print_detail=False)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA, save_limit=100, print_detail=False)
