"""Advent of code 2017
--- Day 9: Stream Processing ---
"""

from common.aoc import file_to_list, aoc_part, get_filename
from common.tree import Node


class GG(Node):
    """A node Group or Garbage"""

    def __init__(self, parent, garbage=None, data=None) -> None:
        super().__init__(parent, data)
        self.garbage = garbage

    @property
    def depth(self):
        """The depth"""
        if self.parent is None:
            return 0
        return self.parent.depth + 1

    @property
    def score(self):
        """Score"""
        score = 0
        if self.garbage is None:
            score = self.depth
        return score + sum(ch.score for ch in self.children)

    @property
    def garbage_count(self):
        """Garbage count"""
        gc = 0
        if self.garbage:
            gc = len(self.garbage)
        return gc + sum(ch.garbage_count for ch in self.children)


def parse_data(raw_data):
    """Parse the input"""
    return raw_data


def tree_of_garbage(stream):
    """Return a tree of groups and garbage"""
    root = GG(None)
    parent = root

    while stream:

        if not stream:
            break
        ch = stream[0]

        if ch == "{":
            parent = GG(parent)
            stream = stream[1:]
            continue
        if ch == "}":
            parent = parent.parent
            stream = stream[1:]
            continue
        if ch == ",":
            stream = stream[1:]
            continue
        if ch == "<":
            i = 0
            garbage = ""
            while True:
                i += 1
                ch = stream[i]
                if ch == ">":
                    break
                if ch == "!":
                    i += 1
                    continue
                garbage += ch
            GG(parent, garbage=garbage)
            stream = stream[i + 1 :]
            continue

    return root


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""

    # Tests
    # for line in data:
    #     root = tree_of_garbage(line)
    #     print(root.score)
    root = tree_of_garbage(data[-1])
    return root.score


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    root = tree_of_garbage(data[-1])
    # root.dump(attrs=["garbage_count", "garbage"])
    return root.garbage_count


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
