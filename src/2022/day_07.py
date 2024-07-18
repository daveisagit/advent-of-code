"""Advent of code 2022
--- Day 7: No Space Left On Device ---
"""

from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


class Directory:
    """Modelling a directory"""

    def __init__(self, name, parent=None) -> None:
        self.name = name
        self.files = {}
        self.sub_folders = {}
        self.parent = parent

    @property
    def size(self):
        return sum(self.files.values()) + sum(
            ch.size for ch in self.sub_folders.values()
        )


def parse_data(raw_data):
    """Build a tree structure where Directory is a node"""
    root = Directory("/")
    cd = root
    for line in raw_data:

        # handle commands
        if line[0] == "$":
            cmd = line[2:4]
            if cmd == "cd":
                dn = line[5:]
                if dn == "/":
                    cd = root
                    continue
                if dn == "..":
                    cd = cd.parent
                    continue
                cd = cd.sub_folders[dn]
                continue
            if cmd == "ls":
                continue
            raise RuntimeError(f"Unexpected $ {cmd}")

        # this must be terminal output
        arr = tok(line)
        if arr[0] == "dir":
            # add the directory
            folder = Directory(arr[1], parent=cd)
            cd.sub_folders[folder.name] = folder
            continue

        # add the file
        cd.files[arr[1]] = int(arr[0])

    return root


def traverse(p: Directory):
    yield p
    for ch in p.sub_folders.values():
        yield from traverse(ch)


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    return sum((d.size) for d in traverse(data) if d.size <= 100000)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    total = 70000000
    required_unused = 30000000
    used = data.size
    unused = total - used
    remove = required_unused - unused
    candidates = [d for d in traverse(data) if d.size >= remove]
    candidates = sorted(candidates, key=lambda x: x.size)
    return candidates[0].size


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
