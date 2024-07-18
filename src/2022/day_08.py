"""Advent of code 2022
--- Day 8: Treetop Tree House ---
"""

from operator import add
from common.aoc import file_to_list, aoc_part, get_filename
from common.grid_2d import directions


def parse_data(raw_data):
    """Return a dictionary keyed on tuple coordinates, with tree height as the
    value"""
    data = {}
    for ri, row in enumerate(raw_data):
        for ci, height in enumerate(row):
            p = (ri, ci)
            data[p] = int(height)
    return data


def get_tree_line(grid, pos, d):
    """Return the list of tree heights from pos going in direction d"""
    tree_line = []
    cp = tuple(map(add, pos, d))
    while cp in grid:
        tree_line.append(grid[cp])
        cp = tuple(map(add, cp, d))
    return tree_line


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    visible_count = 0
    for pos, h in data.items():
        visible = False
        for d in directions.values():
            tree_line = get_tree_line(data, pos, d)
            tall_trees = [t for t in tree_line if t >= h]
            if not tall_trees:
                visible = True
                break
        if visible:
            visible_count += 1

    return visible_count


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    viewing_distances = {}
    for pos, h in data.items():
        viewing_distance = 1
        for d in directions.values():
            tree_line = get_tree_line(data, pos, d)
            viewable_trees = 0  # how many trees can I see in this direction
            for t in tree_line:
                viewable_trees += 1
                if t >= h:
                    break
            viewing_distance *= viewable_trees
        viewing_distances[pos] = viewing_distance

    return max(viewing_distances.values())


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
