"""Advent of code 2018
--- Day 20: A Regular Map ---
"""

from collections import defaultdict, deque
from operator import add
from common.aoc import file_to_string, aoc_part, get_filename
from common.graph import dijkstra
from common.grid_2d import get_grid_limits
from common.tree import Node

directions = {
    "E": (0, 1),
    "N": (-1, 0),
    "W": (0, -1),
    "S": (1, 0),
}


def parse_data(raw_data):
    """Make an AST"""
    root: Node = Node(None, "seq")
    parent = root
    for ch in raw_data[1:-1]:
        if ch not in "(|)":
            n = Node(parent, ch)
            continue

        if ch == "(":
            n = Node(parent, "or")
            n = Node(n, "seq")
            parent = n
            continue

        if ch == "|":
            parent = parent.parent
            n = Node(parent, "seq")
            parent = n
            continue

        if ch == ")":
            parent = parent.parent.parent
            continue

    return root


def make_graph_old(root):
    """Create the graph"""

    gph = defaultdict(dict)

    dfs = deque()
    state = (root, (0, 0), (0,))
    dfs.append(state)
    seen = set()
    while dfs:
        state = dfs.popleft()
        seq, pos, ptr = state
        if (seq, pos, ptr) in seen:
            continue
        seen.add((seq, pos, ptr))
        if ptr[-1] >= len(seq.children):
            ptr = ptr[:-1]
            if len(ptr) > 0:
                ptr = list(ptr)
                ptr[-1] += 1
                state = (seq.parent.parent, pos, tuple(ptr))
                dfs.append(state)
            continue

        n = seq.children[ptr[-1]]
        if n.data != "or":
            d = directions[n.data]
            nxt = tuple(map(add, pos, d))
            gph[pos][nxt] = 1
            # gph[nxt][pos] = 1
            ptr = list(ptr)
            ptr[-1] += 1
            state = (seq, nxt, tuple(ptr))
            dfs.append(state)
            continue

        ptr = list(ptr)
        ptr.append(0)
        for ch in n.children:
            state = (ch, pos, tuple(ptr))
            dfs.append(state)

    return gph


def draw_rooms(gph, just_walls=False):
    """Visual"""
    vdc = "|"
    hdc = "-"
    rc = "."
    if just_walls:
        vdc = " "
        hdc = " "
        rc = " "
    min_r, min_c, max_r, max_c = get_grid_limits(gph)
    width = (max_c - min_c) * 2 + 3
    height = (max_r - min_r) * 2 + 3
    print(height, width)
    row = "#" * width
    print(row)

    for r in range(min_r, max_r + 1):

        row = ["#"] + [rc] * (width - 2) + ["#"]
        for ic, c in enumerate(range(min_c, max_c)):
            p = (r, c)
            q = (r, c + 1)
            if q in gph[p]:
                row[ic * 2 + 2] = vdc
            else:
                row[ic * 2 + 2] = "#"
        print("".join(row))

        row = ["#"] * width
        for ic, c in enumerate(range(min_c, max_c + 1)):
            p = (r, c)
            q = (r + 1, c)
            if q in gph[p]:
                row[ic * 2 + 1] = hdc
        print("".join(row))


def make_graph(root):
    """Create the graph of all locations an edges represent a door"""

    def explore_seq_node(n: Node, pos):
        for cn in n.children:
            if cn.data != "or":
                d = directions[cn.data]
                nxt = tuple(map(add, pos, d))
                gph[pos][nxt] = 1
                gph[nxt][pos] = 1
                pos = nxt
                continue
            for sn in cn.children:
                explore_seq_node(sn, pos)

    gph = defaultdict(dict)
    explore_seq_node(root, (0, 0))
    return gph


@aoc_part
def solve_part_a(root) -> int:
    """Solve part A"""
    # root.dump()
    gph = make_graph(root)
    # draw_rooms(gph, just_walls=True)
    dist = dijkstra(gph, (0, 0), None)
    return max(dist.values())


@aoc_part
def solve_part_b(root) -> int:
    """Solve part B"""
    gph = make_graph(root)
    dist = dijkstra(gph, (0, 0), None)
    at_least_1000_doors = [d for d in dist.values() if d >= 1000]
    return len(at_least_1000_doors)


EX_RAW_DATA = file_to_string(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)


solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(MY_DATA)
