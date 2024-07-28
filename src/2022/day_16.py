"""Advent of code 2022
--- Day 16: Proboscidea Volcanium ---
"""

from collections import defaultdict, deque
import re
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import powerset, tok
from common.graph import get_adjacency_matrix


def parse_data(raw_data):
    """Parse the input"""
    valves = {}
    for line in raw_data:
        rr = re.search(
            r"Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.+)",
            line,
        )
        valve = rr.group(1)
        rate = int(rr.group(2))
        tunnels = tok(rr.group(3), ",")
        valves[valve] = rate, tuple(tunnels)
    return valves


def make_graph(data):
    gph = defaultdict(dict)
    for valve, (_, tunnels) in data.items():
        for t in tunnels:
            gph[valve][t] = 1
            gph[t][valve] = 1
    return gph


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    best = 0
    nodes = {valve for valve, (rate, _) in data.items() if rate > 0}
    nodes.add("AA")
    gph = make_graph(data)
    mtx = get_adjacency_matrix(gph, nodes=nodes)
    if data["AA"][0] == 0:
        nodes.discard("AA")

    state = 0, "AA", 0, frozenset()
    dfs = deque()
    dfs.append(state)
    while dfs:
        state = dfs.pop()
        min, valve, released, open = state

        new_open = set(open)
        if valve != "AA":
            min += 1
            new_open.add(valve)
            to_go = max(30 - min, 0)
            released += data[valve][0] * to_go

        if min >= 30 or new_open == nodes:
            best = max(best, released)
            continue

        for v, d in mtx[valve].items():
            if v == "AA":
                continue
            if v in new_open:
                continue
            state = min + d, v, released, frozenset(new_open)
            dfs.append(state)

    return best


def get_best_for_subset_in_time(mtx, rates, subset, memo, start="AA", time=26):
    """Solve part A"""

    def get_best(pos, to_undo, to_go):

        if (pos, to_undo, to_go) in memo:
            return memo[(pos, to_undo, to_go)]

        best = 0
        for v in to_undo:
            new_to_undo = set(to_undo)
            new_to_undo.discard(v)
            new_to_undo = frozenset(new_to_undo)
            new_to_go = to_go - mtx[pos][v] - 1
            releasing = rates[v] * new_to_go
            if new_to_go > 0 and new_to_undo:
                releasing += get_best(v, new_to_undo, new_to_go)
            best = max(best, releasing)

        memo[(pos, to_undo, to_go)] = best
        return best

    return get_best(start, subset, time)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    gph = make_graph(data)
    nodes = {valve for valve, (rate, _) in data.items() if rate > 0}
    rates = {valve: rate for valve, (rate, _) in data.items()}
    start = "AA"
    nodes.add(start)
    mtx = get_adjacency_matrix(gph, nodes=nodes)
    nodes.discard(start)
    memo = {}

    power_set = {frozenset(subset) for subset in list(powerset(nodes))}
    amount_for_subset = {}
    for subset in power_set:
        amount_for_subset[subset] = get_best_for_subset_in_time(
            mtx, rates, subset, memo
        )

    best = 0
    for subset_a in power_set:
        subset_b = frozenset(nodes - subset_a)
        amount = amount_for_subset[subset_a] + amount_for_subset[subset_b]
        best = max(best, amount)

    return best


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
