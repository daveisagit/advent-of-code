"""Advent of code 2017
--- Day 7: Recursive Circus ---
"""

from collections import Counter
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok
from common.tree import Node


class Program(Node):
    """AS per puzzle"""

    def __init__(self, parent, name, weight) -> None:
        super().__init__(parent)
        self.name = name
        self.weight = weight
        self.total_weight = 0


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        arr = tok(line, "->")
        pv = arr[0]
        supports = []
        if len(arr) > 1:
            supports = tok(arr[1], ",")
        arr = tok(pv)
        pgm = arr[0]
        v = int(arr[1][1:-1])
        data.append((pgm, v, tuple(supports)))

    data = create_tree(data)
    return data


def create_tree(data):
    """Dict and Tree of the programs"""
    nodes = {}
    for pgm, v, _ in data:
        n = Program(None, pgm, v)
        nodes[pgm] = n

    for p, v, supports in data:
        for c in supports:
            if nodes[c].parent:
                print(nodes[c].parent.name, p)
                raise RuntimeError()
            else:
                nodes[c].set_parent(nodes[p])
    return nodes


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    root = list(data.values())[0].root().name
    return root


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""

    def set_total_weight(n: Node):
        tw = 0
        if not n.children:
            n.total_weight = n.weight
            return n.weight
        for ch in n.children:
            tw += set_total_weight(ch)
        n.total_weight = tw + n.weight
        return n.total_weight

    root = list(data.values())[0].root().name
    root = data[root]
    set_total_weight(root)

    cn = root
    while True:

        if not cn.children:
            cn = cn.parent
            break

        cs = [ch.total_weight for ch in cn.children]
        cnt = Counter(cs)
        if len(cnt) == 1:
            cn = cn.parent
            break

        cv = cnt.most_common()[0][0]
        for ch in cn.children:
            if ch.total_weight != cv:
                break
        cn = ch

    cs = [ch.total_weight for ch in cn.children]
    cnt = Counter(cs)
    cv = cnt.most_common()[0][0]
    for ch in cn.children:
        if ch.total_weight != cv:
            adj = cv - ch.total_weight
            ans = ch.weight + adj
            return ans


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
