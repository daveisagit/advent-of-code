"""Advent of code 2019
--- Day 6: Universal Orbit Map ---
"""

from collections import defaultdict
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok
from common.tree import Node, make_tree


def parse_data(raw_data):
    """Parse the input"""
    data = defaultdict(set)
    for line in raw_data:
        arr = tok(line, ")")
        data[arr[0]].add(arr[1])
    return data


def get_checksum(data):
    """For part a"""
    depth_sum = 0
    parents = {}

    def count_orbits(obj, depth=0):
        nonlocal depth_sum
        depth_sum += depth
        for orb in data[obj]:
            parents[orb] = obj
            count_orbits(orb, depth + 1)

    count_orbits("COM")
    return depth_sum, parents


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    ds, _ = get_checksum(data)
    return ds


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    _, parents = get_checksum(data)

    you_ancestors = []
    cur = "YOU"
    while cur in parents:
        cur = parents[cur]
        you_ancestors.append(cur)

    san_ancestors = []
    cur = "SAN"
    while cur in parents:
        cur = parents[cur]
        san_ancestors.append(cur)

    for i, obj in enumerate(you_ancestors):
        if obj in san_ancestors:
            j = san_ancestors.index(obj)
            return i + j

    return None


@aoc_part
def solve_part_c(data) -> int:
    """Solve part A"""
    tree_nodes = make_tree(data)
    root = list(tree_nodes.values())[0].root()
    depth_sum = 0
    for n in root.traverse():
        depth_sum += n.depth
    print(depth_sum)

    n1 = tree_nodes["YOU"]
    n2 = tree_nodes["SAN"]
    return len(n1.path_to(n2)) - 1


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)

solve_part_c(MY_DATA)
