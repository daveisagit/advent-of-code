"""Advent of code 2022
--- Day 24: Blizzard Basin ---
"""

from collections import defaultdict, deque
from operator import add
from common.aoc import file_to_list, aoc_part, get_filename
from common.grid_2d import directions


def parse_data(raw_data):
    """Parse the input"""
    blizzards = defaultdict(set)
    walls = set()
    start = None
    finish = None
    height = len(raw_data)
    for ri, row in enumerate(raw_data):
        width = len(row)
        for ci, content in enumerate(row):
            if content == "#":
                walls.add((ri, ci))
                continue
            if content in "<>^v":
                blizzards[content].add((ri, ci))
            if ri == 0 and content == ".":
                start = ri, ci
            if ri == len(raw_data) - 1 and content == ".":
                finish = ri, ci

    return walls, blizzards, start, finish, height, width


def get_next_blizzard(walls, blizzards, height, width):
    new_blizzards = defaultdict(set)
    for d, ps in blizzards.items():
        dv = directions[d]
        loop = 1
        if d == "^":
            loop = height - 2
        elif d == "<":
            loop = width - 2

        for p in ps:
            np = tuple(map(add, p, dv))
            if np in walls:
                if d in "<>":
                    np = np[0], loop
                else:
                    np = loop, np[1]
            new_blizzards[d].add(np)
    return new_blizzards


def draw_valley(walls, blizzards, height, width):
    print()
    for r in range(height):
        row = ""
        for c in range(width):
            if (r, c) in walls:
                ch = "#"
                row += ch
                continue
            ch = ""
            for d, blizzard in blizzards.items():
                if (r, c) in blizzard:
                    ch += d
            if len(ch) == 0:
                ch = "."
            elif len(ch) > 1:
                ch = str(len(ch))
            row += ch
        print(row)


def travel(walls, blizzards, start, finish, height, width, prev_minute=-1):
    """BFS to find quickest time"""
    bfs = deque()
    state = 0, start
    bfs.append(state)
    seen = set()
    options = list(directions.values()) + [(0, 0)]
    all_blizzards = set()
    for b in blizzards.values():
        all_blizzards.update(b)

    while bfs:
        state = bfs.popleft()
        if state in seen:
            continue
        seen.add(state)
        minute, pos = state

        if pos == finish:
            return minute, blizzards

        if minute > prev_minute:
            prev_minute = minute
            blizzards = get_next_blizzard(walls, blizzards, height, width)
            all_blizzards = set()
            for b in blizzards.values():
                all_blizzards.update(b)

        for d in options:
            np = tuple(map(add, pos, d))
            if np not in walls and np not in all_blizzards and 0 <= np[0] < height:
                new_state = minute + 1, np
                bfs.append(new_state)


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    walls, blizzards, start, finish, height, width = data
    minute, blizzards = travel(walls, blizzards, start, finish, height, width)
    return minute


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    walls, blizzards, start, finish, height, width = data
    t1, blizzards = travel(walls, blizzards, start, finish, height, width)
    t2, blizzards = travel(
        walls, blizzards, finish, start, height, width, prev_minute=t1
    )
    t3, blizzards = travel(
        walls, blizzards, start, finish, height, width, prev_minute=t2
    )
    return t3


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)


solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
