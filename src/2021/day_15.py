"""Advent of code 2021
--- Day 15: Chiton ---
"""

from collections import defaultdict
from operator import add
from common.aoc import file_to_list, aoc_part, get_filename
from common.graph import dijkstra
from common.grid_2d import RC, directions


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        row = [int(c) for c in line]
        data.append(row)
    return data


def make_graph(data):
    """Make a graph of the positions"""
    rows = len(data)
    cols = len(data[0])
    g = defaultdict(dict)
    for ir, row in enumerate(data):
        for ic, v in enumerate(row):
            t_pos = RC(ir, ic)
            for d in directions.values():
                n_pos = RC(*tuple(map(add, t_pos, d)))
                if 0 <= n_pos.row < rows and 0 <= n_pos.col < cols:
                    nv = data[n_pos.row][n_pos.col]
                    g[t_pos][n_pos] = nv
                    g[n_pos][t_pos] = v
    return g


def dump_grid(grid):
    """Visualise the grid"""
    for row in grid:
        print("".join([str(v) for v in row]))


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    rows = len(data)
    cols = len(data[0])
    g = make_graph(data)
    lr = dijkstra(g, (0, 0), (rows - 1, cols - 1))
    return lr


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B - can our algorithm handle the increase in size"""
    rows = len(data)
    cols = len(data[0])

    big_grid = []
    for _ in range(rows * 5):
        long_row = list([0] * (cols * 5))
        big_grid.append(long_row)

    for r in range(5):
        for c in range(5):
            for lr, row in enumerate(data):
                for lc, v in enumerate(row):
                    if r == c == 0:
                        big_grid[lr][lc] = v
                    else:
                        if c > 0:
                            v = big_grid[r * rows + lr][(c - 1) * cols + lc]
                        else:
                            v = big_grid[(r - 1) * rows + lr][c * cols + lc]
                        v += 1
                        if v > 9:
                            v = 1
                        big_grid[r * rows + lr][c * cols + lc] = v

    g = make_graph(big_grid)
    lr = dijkstra(g, (0, 0), (rows * 5 - 1, cols * 5 - 1))

    return lr


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
