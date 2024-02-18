"""Advent of code 2019
--- Day 18: Many-Worlds Interpretation ---
"""

from collections import defaultdict, deque
from math import inf
from operator import add
from common.aoc import file_to_list, aoc_part, get_filename
from common.graph import dijkstra_paths, simplify
from common.grid_2d import directions, diagonal_directions


def parse_data(raw_data):
    """Parse the input
    Return a graph where nodes are doors, keys, start and junctions
    """
    gph = defaultdict(dict)
    path = set()
    keys = {}
    doors = {}
    starts = set()
    for ri, line in enumerate(raw_data):
        for ci, c in enumerate(line):
            p = (ri, ci)
            if c != "#":
                path.add(p)
            if c.isalpha():
                if c.islower():
                    keys[c] = p
                if c.isupper():
                    doors[c] = p
            if c == "@":
                starts.add(p)

    for p in path:
        for d in directions.values():
            n = tuple(map(add, p, d))
            if n in path:
                gph[p][n] = 1

    protected_nodes = starts
    protected_nodes = protected_nodes.union(set(doors.values()))
    protected_nodes = protected_nodes.union(set(keys.values()))
    simplify(gph, protected_nodes=protected_nodes)
    return gph, starts, keys, doors


def get_data_for_analysis(gph, starts, keys):
    """Get all paths up front for the start and each key"""
    places_of_interest = starts | set(keys)
    matrix = {}
    for p in places_of_interest:
        distances, paths = dijkstra_paths(gph, p)
        matrix[p] = {}
        for n, d in distances.items():
            if n == p:
                continue
            matrix[p][n] = (d, paths[n])
    return matrix


def rename_nodes(gph, keys, doors):
    """Return same graph with (r,c) replaced key/door names"""
    g = defaultdict(dict)
    p2k = {p: k for k, p in keys.items()}
    p2d = {p: d for d, p in doors.items()}
    for u, neighbours in gph.items():
        for v, d in neighbours.items():
            if u in p2k:
                u = p2k[u]
            if v in p2k:
                v = p2k[v]
            if u in p2d:
                u = p2d[u]
            if v in p2d:
                v = p2d[v]
            g[u][v] = d
    return g


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""

    def shortest_path(picked_up, cur_pos):
        """Recursive with memoize, we return length or None if no path exists"""
        state = (picked_up, cur_pos)
        if state in best:
            return best[state]

        # we're done return 0 as the starting
        # point for accumulation back up the call stack
        if len(picked_up) == len(keys):
            return 0

        shortest = inf
        open_doors = {k.upper() for k in picked_up}
        for n, vals in m[cur_pos].items():
            if n in picked_up or n not in keys:
                continue
            # we must have a key that's not been picked up yet
            d, p = vals
            # are there any closed doors on our path
            closed_doors = [u for u in p if u in doors and u not in open_doors]
            if closed_doors:
                continue

            # we are permitted to roam from cur_pos to n
            npu = frozenset(set(picked_up) | {n})
            sp = shortest_path(npu, n)
            if sp is not None:
                if sp + d < shortest:
                    shortest = sp + d

        ans = shortest
        if shortest == inf:
            ans = None

        # remember the answer for this state
        best[state] = ans
        return ans

    gph, starts, keys, doors = data
    gph = rename_nodes(gph, keys, doors)
    m = get_data_for_analysis(gph, starts, keys)
    best = {}

    return shortest_path(frozenset(), list(starts)[0])


def solve_part_b_queue(data) -> int:
    """Solve part B using queue, slower"""

    def remove_node(n):
        for u in gph[n]:
            del gph[u][n]
        del gph[n]

    gph, starts, keys, doors = data
    gph = rename_nodes(gph, keys, doors)

    if len(starts) == 1:
        # using our file
        start = starts.pop()
        starts = {tuple(map(add, start, d)) for d in diagonal_directions}

        remove_node(start)
        for d in directions.values():
            rmv = tuple(map(add, start, d))
            remove_node(rmv)

    m = get_data_for_analysis(gph, starts, keys)
    state = (frozenset(), tuple(starts), 0)
    dfs = deque()
    shortest = inf
    dfs.append(state)
    seen = {}
    while dfs:
        state = dfs.popleft()
        picked_up, locations, travelled = state

        if (picked_up, locations) in seen:
            if seen[(picked_up, locations)] <= travelled:
                continue
        seen[(picked_up, locations)] = travelled

        if len(picked_up) == len(keys):
            if travelled < shortest:
                shortest = travelled

        open_doors = {k.upper() for k in picked_up}
        for r in range(4):
            loc = locations[r]
            for n, vals in m[loc].items():
                if n in picked_up or n not in keys:
                    continue
                d, p = vals
                closed_doors = [u for u in p if u in doors and u not in open_doors]
                if closed_doors:
                    continue

                next_picked_up = frozenset(set(picked_up) | {n})
                next_locations = list(locations)
                next_locations[r] = n
                next_state = (
                    next_picked_up,
                    tuple(next_locations),
                    travelled + d,
                )
                dfs.append(next_state)

    return shortest


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""

    def remove_node(n):
        for u in gph[n]:
            del gph[u][n]
        del gph[n]

    def shortest_path(picked_up, locations):

        state = (picked_up, locations)
        if state in best:
            return best[state]

        if len(picked_up) == len(keys):
            return 0

        open_doors = {k.upper() for k in picked_up}
        shortest = inf
        for r in range(4):
            loc = locations[r]
            for n, vals in m[loc].items():
                if n in picked_up or n not in keys:
                    continue
                d, p = vals
                closed_doors = [u for u in p if u in doors and u not in open_doors]
                if closed_doors:
                    continue

                next_picked_up = frozenset(set(picked_up) | {n})
                next_locations = list(locations)
                next_locations[r] = n

                sp = shortest_path(next_picked_up, tuple(next_locations))
                if sp is not None:
                    if sp + d < shortest:
                        shortest = sp + d

            ans = shortest
            if shortest == inf:
                ans = None

        # remember the answer for this state
        best[state] = ans
        return ans

    best = {}
    gph, starts, keys, doors = data
    gph = rename_nodes(gph, keys, doors)

    if len(starts) == 1:
        # using our file
        start = starts.pop()
        starts = {tuple(map(add, start, d)) for d in diagonal_directions}

        remove_node(start)
        for d in directions.values():
            rmv = tuple(map(add, start, d))
            remove_node(rmv)

    m = get_data_for_analysis(gph, starts, keys)

    return shortest_path(frozenset(), tuple(starts))


EX_RAW_DATA = file_to_list(get_filename(__file__, "xa"))
EX_DATA_A = parse_data(EX_RAW_DATA)

EX_RAW_DATA = file_to_list(get_filename(__file__, "xb"))
EX_DATA_B = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA_A)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA_B)
solve_part_b(MY_DATA)
