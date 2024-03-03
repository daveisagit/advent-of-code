"""Advent of code 2018
--- Day 8: Memory Maneuver ---
"""

from collections import defaultdict
from common.aoc import file_to_string, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    data = [int(x) for x in tok(raw_data)]
    return data


def get_tree(data):
    """Return the nodes as an array with parent/children dictionaries"""

    def parse_list(p, L):
        child_count = L[0]
        meta_count = L[1]
        L = L[2:]

        next_node = len(nodes)
        nodes.append(None)

        if p is not None:
            parent[next_node] = p
            children[p].append(next_node)

        for _ in range(child_count):
            L = parse_list(next_node, L)

        nodes[next_node] = L[:meta_count]
        L = L[meta_count:]

        return L

    nodes = []
    parent = {}
    children = defaultdict(list)
    parse_list(None, data)
    return nodes, parent, children


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    nodes, _, _ = get_tree(data)
    return sum(sum(meta) for meta in nodes)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""

    def node_value(n):
        if len(children[n]) == 0:
            return sum(nodes[n])
        val = 0
        for child_index in nodes[n]:
            idx = child_index - 1
            if 0 <= idx < len(children[n]):
                val += node_value(children[n][idx])
        return val

    nodes, _, children = get_tree(data)

    return node_value(0)


EX_RAW_DATA = file_to_string(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
