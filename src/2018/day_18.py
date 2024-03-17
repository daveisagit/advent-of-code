"""Advent of code 2018
--- Day 18: Settlers of The North Pole ---
"""

from collections import Counter, defaultdict
from itertools import pairwise
import json
from operator import add
from common.aoc import file_to_list, aoc_part, get_filename
from common.grid_2d import all_directions


def parse_data(raw_data):
    """Parse the input"""
    landscape = {}
    height = len(raw_data)
    width = len(raw_data[0])
    for r, line in enumerate(raw_data):
        for c, ch in enumerate(line):
            p = (r, c)
            landscape[p] = ch
    return height, width, landscape


def draw(height, width, landscape):
    """Visual"""
    for r in range(height):
        row = ""
        for c in range(width):
            p = (r, c)
            row += landscape[p]
        print(row)
    print()


def iterate(height, width, landscape):
    new_landscape = {}
    for r in range(height):
        for c in range(width):
            p = (r, c)
            ct = landscape[p]

            cnt = defaultdict(int)
            for d in all_directions:
                ap = tuple(map(add, p, d))
                ch = landscape.get(ap)
                if ch:
                    cnt[ch] += 1

            new_landscape[p] = ct
            if landscape[p] == ".":
                if cnt["|"] >= 3:
                    new_landscape[p] = "|"
            if landscape[p] == "|":
                if cnt["#"] >= 3:
                    new_landscape[p] = "#"
            if landscape[p] == "#":
                if cnt["#"] >= 1 and cnt["|"] >= 1:
                    new_landscape[p] = "#"
                else:
                    new_landscape[p] = "."

    return new_landscape


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    height, width, landscape = data
    for i in range(10):
        landscape = iterate(height, width, landscape)
        # print(i + 1)
        # draw(height, width, landscape)

    cnt = Counter(landscape.values())
    ans = cnt["|"] * cnt["#"]
    return ans


def analysis(data):
    """Find a repeated state"""

    def get_state():
        s = ""
        for r in range(height):
            for c in range(width):
                p = (r, c)
                s += landscape[p]
        return s

    height, width, landscape = data
    st = get_state()
    states = [st]
    i = 0
    while True:
        landscape = iterate(height, width, landscape)
        i += 1
        st = get_state()
        if st in states:
            return states.index(st), i, states
        states.append(st)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    when = 1000000000
    a, b, states = analysis(data)
    m = b - a
    cc = (when - a) % m
    state = states[cc + a]
    cnt = Counter(state)
    ans = cnt["|"] * cnt["#"]
    return ans


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(MY_DATA)
