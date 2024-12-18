"""Useful snips"""

from collections import deque
from operator import add
import re

# ----------------
# regex
# ----------------

# chars needing escaping
# \ ^ $ . + * ? | () [] {}

# https://regex101.com/

"""
Finished\? matches “Finished?”
^http matches strings that begin with http
[^0-9] matches any character not 0-9
ing$ matches “exciting” but not “ingenious”
gr.y matches “gray“, “grey”
Red|Yellow matches “Red” or “Yellow”
colou?r matches colour and color
Ah? matches “Al” or “Ah”
Ah* matches “Ahhhhh” or “A”
Ah+ matches “Ah” or “Ahhh” but not “A”
[cbf]ar matches “car”, “bar”, or “far”
[a-zA-Z] matches ascii letters a-z (uppercase and lower case)

2016 - Day 9 : forcing first find
"""

raw_data = ""

for line in raw_data:
    sr = re.search(r"(.+) to (.+) = (\d+)", line)
    sr = re.search(r"(.{3}) = \((.{3}), (.{3})\)", line)
    sr = re.search(r"(\d+)-(\d+),(\d+)-(\d+)", line)
    sr = re.search(r"pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)", line)
    u = sr.group(1)
    v = sr.group(2)
    d = int(sr.group(3))
    tuple(int(g) for g in sr.groups())

    # based on
    # list_2d_to_dict(list_2d, poi_labels=None, replace_poi_with_char=None)

    grid = {}
    bot = None
    sz = len(raw_data), len(raw_data[0])
    for ri, row in enumerate(raw_data):
        for ci, ch in enumerate(row):
            p = (ri, ci)
            if ch == "@":
                bot = p
                ch = "."
            grid[p] = ch
    # return sz, grid, bot

# ----------------
# BFS
# Day 10 has recursion too
# ----------------

bfs = deque()
seen = set()
state = 1, 2, 3
bfs.append(state)
while bfs:
    state = bfs.popleft()
    a, b, c = state
    if state in seen:
        continue
    seen.add(state)

    # check if target reached

    # check if unreachable?

    # add options to queue
    for _ in {}:
        new_state = list(state)
        new_state[0] = 2
        new_state = tuple(new_state)
        bfs.append(new_state)

# ----------------
# Heap
# ----------------

from heapq import heappush, heappop

h = []
# state = Priority,x, y, z, etc
state = 0, 0, 0, 0
heappush(h, state)
seen = set()
while h:
    state = heappop(h)
    if state in seen:
        continue
    seen.add(state)

    # check if target reached

    # check if unreachable

    # add options to heap
    for _ in {}:
        state = 0, 0, 0, 0
        heappush(h, state)

# ------------------------------
# Directions, Grids and Graphs
# ------------------------------

ALPHA_LOWER = "abcdefghijklmnopqrstuvwxyz"
ALPHA_UPPER = ALPHA_LOWER.upper()
DIGITS = "0123456789"
labels = set(list(ALPHA_LOWER) + list(ALPHA_UPPER) + list(DIGITS))

from common.visuals import visualize_graph
from common.grid_2d import (
    directions,
    list_2d_to_dict,
    maze_to_graph,
)
from common.graph import dijkstra

p = (0, 0)
for dc, dv in directions.items():
    np = tuple(map(add, p, dv))

    if all(0 <= x < sz for x in np):
        pass


sz, grid, poi = list_2d_to_dict(raw_data, poi_labels=None, replace_poi_with_char=None)
start = poi["A"]
target = poi["Z"]
gph = maze_to_graph(start, grid, directed=False, path_char=".", node_chars="")
visualize_graph(gph, directed=False)
dst = dijkstra(gph, start, target, weight_attr=None)

# in case we need it
from numpy.linalg import matrix_rank


def are_parallel(a, b):
    """Return True if the vectors are parallel"""
    vectors = [a, b]
    r = matrix_rank(vectors)
    return r <= 1


# in case we need it
import networkx as nx
from common.graph import directed_edges

de = directed_edges(gph)
G = nx.from_edgelist(de)
