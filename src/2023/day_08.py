"""Advent of code 2023
--- Day 8: Haunted Wasteland ---
"""

from math import lcm
import re
from common.aoc import file_to_list, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    turns = [0 if ch == "L" else 1 for ch in raw_data[0]]
    nodes = {}
    for line in raw_data[2:]:
        sr = re.search(r"(.{3}) = \((.{3}), (.{3})\)", line)
        nodes[sr.group(1)] = (sr.group(2), sr.group(3))
    return turns, nodes


def move_count(nodes: dict, start: str, finish: str, turns: list) -> int:
    turn_index = 0
    moves = 0
    cur = start
    while cur != finish:
        cur = nodes[cur][turns[turn_index]]
        turn_index += 1
        turn_index %= len(turns)
        moves += 1
    return moves


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    turns, nodes = data
    return move_count(nodes, "AAA", "ZZZ", turns)


def move_counts_to_z(nodes: dict, start: str, turns: list) -> int:
    turn_index = 0
    moves = 0
    cur = start
    z_moves = {}
    while True:
        if cur[2] == "Z":
            if cur in z_moves:
                break
            z_moves[cur] = moves
        cur = nodes[cur][turns[turn_index]]
        turn_index += 1
        turn_index %= len(turns)
        moves += 1
    return moves, z_moves


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    turns, nodes = data
    start_nodes = {n for n in nodes if n[2] == "A"}
    cycles = [move_counts_to_z(nodes, n, turns) for n in start_nodes]

    # turns out that all of the ghosts return back to their start upon
    # reaching the z node
    if len(cycles) > 1:
        assert all(r == 2 * list(z_moves.values())[0] for r, z_moves in cycles)

    loops = [list(c.values())[0] for _, c in cycles]
    return lcm(*loops)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
