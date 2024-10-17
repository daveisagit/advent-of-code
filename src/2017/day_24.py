"""Advent of code 2017
--- Day 24: Electromagnetic Moat ---
"""

from collections import deque
from heapq import heappop, heappush
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    components = set()
    for line in raw_data:
        component = tuple(int(x) for x in tok(line, "/"))
        components.add(component)
    return frozenset(components)


def get_strongest_bridge_old(components):
    """Find the strongest"""
    dfs = deque()
    dfs.append(([], 0))

    strongest = 0
    while dfs:
        chain, port = dfs.pop()
        strength = sum(sum(c) for c in chain)
        strongest = max(strongest, strength)

        available = set(components)
        used = set(chain)
        available.difference_update(used)
        options = [cmp for cmp in available if port in cmp]
        for opt in options:
            new_chain = chain.copy()
            new_chain.append(opt)
            ports = list(opt)
            ports.remove(port)
            new_port = ports[0]
            dfs.append((new_chain, new_port))

    return strongest


def get_strongest_bridge(components):
    """Using a heap and ignoring routes that will never improve
    Doubt this will apply to part B where longest is not weighted
    """
    available = sum(a + b for a, b in components)
    strongest = 0
    h = []
    # state = -len, chain, port, available
    state = 0, frozenset(), 0, available
    heappush(h, state)

    while h:
        state = heappop(h)
        strength, chain, port, available = state
        strength = -strength

        strongest = max(strongest, strength)

        if strength + available <= strongest:
            continue

        options = [cmp for cmp in components if port in cmp and cmp not in chain]
        for opt in options:
            val = sum(opt)
            new_chain = frozenset(chain | {opt})
            new_port = opt[0]
            if new_port == port:
                new_port = opt[1]
            state = -strength - val, new_chain, new_port, available - val
            heappush(h, state)

    return strongest


@aoc_part
def solve_part_a(components) -> int:
    """Solve part A"""
    return get_strongest_bridge(components)


def get_longest_bridge(components):
    """Find the longest"""
    dfs = deque()
    dfs.append(([], 0))

    longest = 0
    longest_strength = 0
    while dfs:
        chain, port = dfs.pop()
        strength = sum(sum(c) for c in chain)

        if len(chain) >= longest:
            if len(chain) > longest:
                longest_strength = strength
            else:
                longest_strength = max(longest_strength, strength)
            longest = len(chain)

        available = set(components)
        used = set(chain)
        available.difference_update(used)
        options = [cmp for cmp in available if port in cmp]
        for opt in options:
            new_chain = chain.copy()
            new_chain.append(opt)
            ports = list(opt)
            ports.remove(port)
            new_port = ports[0]
            dfs.append((new_chain, new_port))

    return longest_strength


@aoc_part
def solve_part_b(components) -> int:
    """Solve part B"""
    return get_longest_bridge(components)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)
print(EX_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)
print(MY_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
