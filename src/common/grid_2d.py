"""Useful things for 2D grids"""

from collections import defaultdict, deque, namedtuple
from itertools import pairwise
from operator import add, sub

directions = {
    ">": (0, 1),
    "^": (-1, 0),
    "<": (0, -1),
    "v": (1, 0),
}

directions_UDLR = {
    "R": (0, 1),
    "U": (-1, 0),
    "L": (0, -1),
    "D": (1, 0),
}

# Index changes
# +1 ACW - left
# -1  CW - right
# 0: East, 1:North, 2:West 3:South
rotations = [(0, 1), (-1, 0), (0, -1), (1, 0)]


def rotate90(v, about=(0, 0)):
    """Rotate anticlockwise 90"""
    return (-v[1], v[0])


compass = {cp: v for cp, v in zip(list("ENWS"), rotations)}

diagonal_directions = ((1, 1), (1, -1), (-1, 1), (-1, -1))
orthogonal_directions = directions.values()
all_directions = list(orthogonal_directions) + list(diagonal_directions)

XY = namedtuple(
    "XY",
    [
        "x",
        "y",
    ],
)

Line = namedtuple(
    "Line",
    [
        "a",
        "b",
    ],
)


RC = namedtuple(
    "RC",
    [
        "row",
        "col",
    ],
)


def get_grid_limits(point_tuples):
    """Return the limits of the data"""
    if not point_tuples:
        return 0, 0, 0, 0
    min_x = min(point[0] for point in point_tuples)
    max_x = max(point[0] for point in point_tuples)
    min_y = min(point[1] for point in point_tuples)
    max_y = max(point[1] for point in point_tuples)
    return min_x, min_y, max_x, max_y
    # for clients using (r,c)
    # min_r, min_c, max_r, max_c


def draw_grid(grid):
    """Visual for list of list single char"""
    for row in grid:
        print("".join(row))


def rotate_grid(sg):
    """Rotate a square grid 90 ACW"""
    rows = len(sg)
    cols = len(sg[0])
    og = []
    for _ in range(cols):
        l = [None] * rows
        og.append(l)
    for ri, row in enumerate(sg):
        for ci, c in enumerate(row):
            og[cols - ci - 1][ri] = c
    return og


def flip_h_grid(sg):
    """Flip horizontally across a vertical axis"""
    og = []
    for row in sg:
        r = list(reversed(row))
        og.append(r)
    return og


def dihedral_arrangements(sg):
    """Generator for the 8 arrangements of a square grid
    returns a triple a,b,grid where a is the number of rotations and b reflections"""
    # Rotate 4 times
    # Reflect and rotate 4 times again
    for a in range(4):
        yield a, 0, sg
        sg = rotate_grid(sg)

    sg = flip_h_grid(sg)
    for a in range(4):
        yield a, 1, sg
        sg = rotate_grid(sg)


def manhattan(p, rel=(0, 0)):
    """Return the manhattan distance"""
    p = tuple(map(sub, p, rel))
    return abs(p[0]) + abs(p[1])


def grid_lists_to_dict(grid, content_filter=None):
    """Given list of list, return dict of coord tuple"""
    new_grid = {}
    for ri, row in enumerate(grid):
        for ci, content in enumerate(row):
            if content_filter:
                if content not in content_filter:
                    continue
            p = (ri, ci)
            new_grid[p] = content
    return new_grid


def window_over_grid(grid, window, step):
    """Generator for a window over a 2D grid"""
    rows = len(grid)
    cols = len(grid[0])
    for row_idx in range(0, rows - window[0] + 1, step[0]):
        for col_idx in range(0, cols - window[1] + 1, step[1]):
            window = []
            row_slice = grid[row_idx : row_idx + window[0]]
            for row in row_slice:
                window.append(row[col_idx : col_idx + window[1]])
            yield window


def transpose(grid):
    """Transpose [][]"""
    return list(map(list, zip(*grid)))


def shoelace_area(outline) -> int:
    """Return the area of the outlined polygon"""
    corners = list(outline)
    if corners[0] != corners[-1]:
        corners.append(corners[0])
    areas = [
        (side[0][0] + side[1][0]) * (side[0][1] - side[1][1])
        for side in pairwise(corners)
    ]
    return abs(sum(areas) // 2)


def maze_to_graph_v1(start, maze):
    """Take a maze expressed as a set of path points and return a
    graph of it"""
    gph = defaultdict(dict)
    bfs = deque()
    # state is from_node, edge_cost, prv, cur
    state = None, 0, None, start
    bfs.append(state)
    while bfs:

        state = bfs.popleft()
        from_node, edge_cost, prv, cur = state

        # what are the choices
        choices = set()
        for dv in directions.values():
            nxt = tuple(map(add, cur, dv))
            if nxt not in maze:
                continue
            choices.add(nxt)

        if len(choices) == 2:
            # if choices = 2 we are on an edge
            # we don't want to turn around
            choices.discard(prv)
        else:
            # otherwise we are on a node
            # record the completed edge
            if from_node:
                gph[from_node][cur] = edge_cost

            # if we've already been here
            if cur in gph:
                continue

            # this is new from_node
            from_node = cur
            edge_cost = 0

        # put the choices on the queue
        for nxt in choices:
            new_state = from_node, edge_cost + 1, cur, nxt
            bfs.append(new_state)

    return gph


def maze_to_graph(start, maze, directed=False, path_char="."):
    """Take a maze expressed as a dict of path points the value
    being either a normal path or a specific direction (<>^v)
    and return a directed graph of it.
    If directed is false then all edges modelled as 2 directed edges"""
    gph = defaultdict(dict)
    bfs = deque()
    # state is from_node, edge_cost, prv, cur
    state = None, 0, None, start
    bfs.append(state)
    while bfs:

        state = bfs.popleft()
        from_node, edge_cost, prv, cur = state

        # what are the choices
        deg = 0
        choices = set()
        for d, dv in directions.items():
            nxt = tuple(map(add, cur, dv))
            if nxt not in maze:
                continue
            deg += 1
            if not directed or maze[nxt] == path_char or maze[nxt] == d:
                choices.add(nxt)

        if deg == 2:
            # if choices = 2 we are on an edge
            # we don't want to turn around
            choices.discard(prv)
        else:
            # otherwise we are on a node
            # record the completed edge
            if from_node:
                gph[from_node][cur] = edge_cost

            # if we've already been here
            if cur in gph:
                continue

            # this is new from_node
            from_node = cur
            edge_cost = 0

        # put the choices on the queue
        for nxt in choices:
            new_state = from_node, edge_cost + 1, cur, nxt
            bfs.append(new_state)

    return gph


def generate_N2(limit=None):
    """Generator for natural lattice"""
    d = 0
    while limit is None or d <= limit:
        for x in range(d + 1):
            yield x, d - x
        d += 1


def generate_Z2(limit=None, origin=(0, 0)):
    """Generator for integer lattice"""
    for p in generate_N2(limit):
        p = (p[0] + origin[0], p[1] + origin[1])
        yield p
        if p[0] != 0:
            yield -p[0], p[1]
        if p[1] != 0:
            yield p[0], -p[1]
        if p[0] and p[1]:
            yield -p[0], -p[1]
