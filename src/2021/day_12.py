"""Advent of code 2021
--- Day 12: Passage Pathing ---
"""

from collections import Counter, defaultdict, deque
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    data = defaultdict(dict)
    for line in raw_data:
        edge = tok(line, delim="-")
        data[edge[0]][edge[1]] = 1
        data[edge[1]][edge[0]] = 1
    return data


def all_paths(data, allow_a_single_second_visit=False):
    """Return all the paths between start and end"""
    stk = deque()
    stk.append(["start"])
    paths = []
    while stk:
        cur_path = stk.pop()
        cur_cave = cur_path[-1]
        for nxt_cave in data[cur_cave]:
            if nxt_cave.lower() == nxt_cave and nxt_cave in cur_path:
                if nxt_cave == "start":
                    continue
                if allow_a_single_second_visit:
                    small_caves = [c for c in cur_path if c.lower() == c]
                    cnt = Counter(small_caves)
                    if cnt.most_common(1)[0][1] > 1:
                        continue
                else:
                    continue

            nxt_path = cur_path.copy()
            nxt_path.append(nxt_cave)
            if nxt_cave == "end":
                paths.append(nxt_path)
                continue
            stk.append(nxt_path)
    return paths


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    paths = all_paths(data)
    return len(paths)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    paths = all_paths(data, allow_a_single_second_visit=True)
    return len(paths)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
