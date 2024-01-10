"""Advent of code 2021
--- Day 18: Snailfish ---
"""

from collections import deque
from common.aoc import file_to_list, aoc_part, get_filename


class TreeNode:
    """Node of binary tree"""

    def __init__(self, parent=None) -> None:
        self.parent: TreeNode | None = parent
        self.left: TreeNode | None = None
        self.right: TreeNode | None = None
        self.value: int | None = None

    @staticmethod
    def load(desc: list | int, parent=None):
        """Given a nested list"""
        n = TreeNode(parent)

        if isinstance(desc, list):
            left = desc[0]
            right = desc[1]
            n.left = TreeNode.load(left, parent=n)
            n.right = TreeNode.load(right, parent=n)

        if isinstance(desc, int):
            n.value = desc

        return n

    def __add__(self, other):
        """Add 2 Snail Fish numbers together"""
        new_node = TreeNode()
        new_node.left = self
        new_node.right = other
        self.parent = new_node
        other.parent = new_node
        new_node.reduce()
        return new_node

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        if self.value is None:
            return f"[{str(self.left)},{str(self.right)}]"
        return str(self.value)

    def depth(self):
        """The depth of a node, root is 0"""
        if self.parent:
            return self.parent.depth() + 1
        return 0

    def root(self):
        """Root node"""
        tn = self
        while tn.parent:
            tn = tn.parent
        return tn

    def leaves(self):
        """All leaves that are a descendent from here"""
        leaves = []
        stk = deque()
        stk.append(self)
        while stk:
            cur = stk.pop()
            if cur.value is None:
                stk.append(cur.right)
                stk.append(cur.left)
            else:
                leaves.append(cur)

        return leaves

    def first_pair_of_depth_from_left(self, depth):
        """Find the first pair of this depth from here"""
        stk = deque()
        stk.append(self)
        while stk:
            cur = stk.pop()
            if cur.value is None:
                if cur.depth() == depth:
                    return cur
                stk.append(cur.right)
                stk.append(cur.left)

        return None

    def first_leaf_left(self):
        """The first leaf to the left"""
        start_at = self
        while start_at.parent:
            if start_at.parent.right == start_at:
                break
            start_at = start_at.parent

        start_at = start_at.parent

        if not start_at:
            return None

        leaves = start_at.left.leaves()
        if not leaves:
            return None
        return leaves[-1]

    def first_leaf_right(self):
        """The first leaf to the right"""
        start_at = self
        while start_at.parent:
            if start_at.parent.left == start_at:
                break
            start_at = start_at.parent

        start_at = start_at.parent

        if not start_at:
            return None

        leaves = start_at.right.leaves()
        if not leaves:
            return None
        return leaves[0]

    def explode(self):
        """Explode this pair"""
        if self.value is not None:
            raise ValueError("Expected a pair")
        fl = self.first_leaf_left()
        if fl:
            fl.value += self.left.value

        fr = self.first_leaf_right()
        if fr:
            fr.value += self.right.value

        self.value = 0
        self.left = None
        self.right = None

    def split(self):
        """Split this node"""
        if self.value is None:
            raise ValueError("Expected a value")
        left = self.value // 2
        right = self.value - left
        self.value = None
        self.left = TreeNode(parent=self)
        self.left.value = left
        self.right = TreeNode(parent=self)
        self.right.value = right

    def reduce(self):
        """Reduce the sailfish"""
        while True:
            tn = self.first_pair_of_depth_from_left(4)
            if tn:
                tn.explode()
                continue
            lvs_over_9 = [leaf for leaf in self.leaves() if leaf.value > 9]
            if lvs_over_9:
                lvs_over_9[0].split()
                continue
            break

    def magnitude(self):
        """Magnitude"""
        if self.value is None:
            return 3 * self.left.magnitude() + 2 * self.right.magnitude()
        return self.value


def parse_data(raw_data):
    """Parse the input, use eval to get an easy list of nested lists"""
    data = []
    for line in raw_data:
        desc = eval(line)
        data.append(desc)
    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    total = TreeNode.load(data[0])
    for snail_fish in data[1:]:
        total += TreeNode.load(snail_fish)
    return total.magnitude()


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    max_mag = 0
    for ia, snail_fish_a in enumerate(data):
        for ib, snail_fish_b in enumerate(data):
            if ia == ib:
                continue
            tn = TreeNode.load(snail_fish_a) + TreeNode.load(snail_fish_b)
            mag = tn.magnitude()
            if mag > max_mag:
                max_mag = mag
    return max_mag


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
