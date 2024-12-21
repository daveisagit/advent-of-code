"""Advent of code 2024
--- Day 21: Keypad Conundrum ---
"""

from functools import lru_cache

from heapq import heappop, heappush
from itertools import product
from math import inf
from operator import add

from common.aoc import file_to_list, aoc_part, get_filename
from common.general import window_over
from common.grid_2d import directions

numpad = "789456123 0A"
dirpad = " ^A<v>"

num_grid = {}
for ri, row in enumerate(window_over(numpad, 3, 3)):
    for ci, content in enumerate(row):
        p = (ri, ci)
        num_grid[p] = content
dir_grid = {}
for ri, row in enumerate(window_over(dirpad, 3, 3)):
    for ci, content in enumerate(row):
        p = (ri, ci)
        dir_grid[p] = content


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        data.append(list(line))
    return data


def get_best_sequences(p, req_ch, grid):
    """Return a list of the best sequences (seq,p)
    where p is the position on the grid"""
    h = []
    # state = len, pos
    state = 0, (), p
    heappush(h, state)
    seen = set()
    seqs = []
    best = None
    while h:
        state = heappop(h)
        l, seq, p = state
        if seq in seen:
            continue
        seen.add(seq)

        if p not in grid:
            continue

        # check if target reached
        if grid[p] == req_ch:
            seq = seq + ("A",)
            if not seqs:
                seqs.append((seq, p))
                best = l
            else:
                if l == best:
                    seqs.append((seq, p))

        # check if unreachable
        if best is not None and l > best:
            return seqs

        # add options to heap
        for dc, dv in directions.items():
            np = tuple(map(add, p, dv))
            if np not in grid:
                continue
            if grid[np] == " ":
                continue
            new_state = l + 1, seq + (dc,), np
            heappush(h, new_state)

    return seqs


def get_num_pad_options(to_make, grid, st):
    """Return all the options for a complete sequence"""
    p1 = st
    all_ways = []
    for ch in to_make:
        ways = []
        for seq, p1 in get_best_sequences(p1, ch, grid):
            ways.append(seq)
        all_ways.append(ways)

    combos = []
    for o in product(*all_ways):
        s = [i for sub in o for i in sub]
        combos.append(s)
    return combos


def get_for_a(val) -> int:
    """Solve part A"""

    # nested loops to find the best option, mmm not great

    best = inf
    opts = get_num_pad_options(val, num_grid, (3, 2))

    for o in opts:
        opts = get_num_pad_options(o, dir_grid, (0, 2))

        for o in opts:
            opts = get_num_pad_options(o, dir_grid, (0, 2))

            for o in opts:
                if len(o) < best:
                    best = len(o)
    return best


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    t = 0
    for v in data:
        n = int("".join(v[:3]))
        b = get_for_a(v)
        t += n * b
    return t


@lru_cache(maxsize=None)
def get_length(p, seq, depth, use_dir_grid=False):
    """Return the ultimate shortest sequence length to fulfil
    this sequence from a point (p) for a given depth
    Use the num pad grid by default.
    Calls itself recursively with memoise
    """

    # establish which keypad grid to use
    grid = num_grid
    if use_dir_grid:
        grid = dir_grid

    # an empty sequence as no length
    # this terminates the recursion
    if not seq:
        return 0

    # use the part A function to get the best sequences
    # to req_ch
    req_ch = seq[0]
    seqs = get_best_sequences(p, req_ch, grid)
    # seqs is a list of tuples (seq,p)
    # where seq is one of the best to get to np
    # np is the new point we will be at on the pad
    np = seqs[0][1]

    if depth == 0:
        # we are the last robot so the best length
        # is any of the best sequences to reach the
        # required character
        best = seqs[0][0]
        # we now serially add movement for the contents of seq
        return len(best) + get_length(np, seq[1:], depth, use_dir_grid=use_dir_grid)

    # consider all the best sequences
    # and for each how long it would take recursively
    # the lower level bots always start at A = (0,2)
    # since that is where they would of finished in order
    # to enter for the level above
    options = []
    for seq1, _ in seqs:
        best = get_length((0, 2), seq1, depth - 1, use_dir_grid=True)
        options.append(best)

    # similarly as at level 0 we serially
    min_len = min(options)
    return min_len + get_length(np, seq[1:], depth, use_dir_grid=use_dir_grid)


@aoc_part
def solve_part_b(data, depth=2) -> int:
    """Solve part B"""
    t = 0
    for v in data:
        n = int("".join(v[:3]))
        l = get_length((3, 2), tuple(v), depth)
        t += n * l

    return t


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
# part A code takes 6s for example and > 1 min for MY_DATA
# We can use part B with 2 directional robots as the same solution
solve_part_b(EX_DATA, depth=2)

# Part A performance on MY_DATA is 2ms
solve_part_b(MY_DATA, depth=2)
# Part B performance on MY_DATA is 10ms
solve_part_b(MY_DATA, depth=25)
