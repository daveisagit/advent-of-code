"""Advent of code 2020
--- Day 7: Handy Haversacks ---
"""

from collections import defaultdict, deque
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""

    can_contain = defaultdict(dict)
    can_be_inside = defaultdict(dict)

    for line in raw_data:
        arr = tok(line, "bags contain")
        container = arr[0]
        container = tuple(tok(container))
        contents = tok(arr[1], ",")
        for content in contents:
            if "no other bags" in content:
                can_contain[container] = {}
                continue

            arr = tok(content)
            qty = int(arr[0])
            ns = (arr[1], arr[2])

            can_contain[container][ns] = qty
            can_be_inside[ns][container] = qty

    return can_contain, can_be_inside


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    _, can_be_inside = data
    bfs = deque()
    seen = set()
    bfs.append(("shiny", "gold"))
    while bfs:
        ns = bfs.popleft()
        if ns in seen:
            continue
        seen.add(ns)
        for outer_ns in can_be_inside[ns]:
            bfs.append(outer_ns)

    return len(seen) - 1


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    # visit every node using depth first search (dfs)
    # multiplying up the number of bags
    can_contain, _ = data

    bags_required = defaultdict(int)
    bfs = deque()
    sg = ("shiny", "gold")
    state = ([sg], 1)
    bfs.append(state)

    while bfs:
        state = bfs.pop()
        cur_path, qty = state
        cur_ns = cur_path[-1]
        bags_required[cur_ns] += qty

        for inner_ns, inner_qty in can_contain[cur_ns].items():
            nxt_path = cur_path.copy()
            nxt_path.append(inner_ns)
            state = (nxt_path, qty * inner_qty)
            bfs.append(state)

    return sum(bags_required.values()) - 1


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
