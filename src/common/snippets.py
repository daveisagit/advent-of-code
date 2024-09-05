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
    u = sr.group(1)
    v = sr.group(2)
    d = int(sr.group(3))
    tuple(int(g) for g in sr.groups())

# ----------------
# BFS
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

    for _ in {}:
        new_state = list(state)
        new_state[0] = 2
        new_state = tuple(new_state)
        bfs.append(new_state)


# ----------------
# Directions
# ----------------
from common.grid_2d import directions

p = (0, 0)
for d, dv in directions:
    np = tuple(map(add, p, dv))
