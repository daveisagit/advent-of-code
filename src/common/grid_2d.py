"""Useful things for 2D grids"""

from collections import defaultdict, deque, namedtuple
from itertools import islice, pairwise
from math import ceil, sqrt
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


def maze_to_graph(start, maze, directed=False, path_char=".", node_chars=""):
    """Take a maze expressed as a dict of path points the value
    being either a normal path or a specific direction (<>^v)
    and return a directed graph of it.
    If directed is false then all edges modelled as 2 directed edges.
    Force nodes via node_chars
    """
    gph = defaultdict(dict)
    bfs = deque()
    seen = set()

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
            if (
                not directed
                or maze[nxt] in path_char
                or maze[nxt] == d
                or maze[nxt] in node_chars
            ):
                choices.add(nxt)

        if deg == 2 and maze[cur] not in node_chars:
            # if choices = 2 we are on an edge
            # we don't want to turn around
            choices.discard(prv)
        else:
            # otherwise we are on a node
            # record the best completed edge
            if from_node:
                if from_node in gph and cur in gph[from_node]:
                    edge_cost = min(edge_cost, gph[from_node][cur])
                gph[from_node][cur] = edge_cost

            # if we've already been here
            if cur in seen:
                continue

            # this is new from_node
            from_node = cur
            edge_cost = 0
            seen.add(cur)

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


def diamond_manhattan_sides(p, d):
    """Return 4 sides (2 pairs of 2 opposite parallel lines) of a diamond
    defined by a centre and manhattan distance.

    similar to the notion of rotating a 2D diamond into a square.

    Each entry is a 2-tuple of the lower and upper manhattan distances
    from the origin.

    Use the pythonic standard on expressing the upper limit as exclusive"""
    x, y = p
    pl = (
        x + y,
        x - y,
    )
    return tuple((p - d, p + d + 1) for p in pl)


def dialines_to_point_set(dialines):
    """Assuming dialines have been created as in diamond_manhattan_sides
    dim 1: 🡕+
    dim 2: 🡖+
    away from origin, then this is the inverse translation giving the set
    of lattice points inside the dialines
    """
    possible_points = set()
    for i0 in range(dialines[0][0], dialines[0][1]):
        for i1 in range(dialines[1][0], dialines[1][1]):
            x = i0 + i1
            y = i0 - i1
            if x % 2 == 0 and y % 2 == 0:
                x = x // 2
                y = y // 2
                d0 = x + y
                d1 = x - y
                if (
                    dialines[0][0] <= d0 < dialines[0][1]
                    and dialines[1][0] <= d1 < dialines[1][1]
                ):
                    # x,y are legitimate
                    possible_points.add((x, y))
    return possible_points


#
# sets of points
#


def set_translate(g, v):
    ng = set()
    for p in g:
        q = tuple(map(add, p, v))
        ng.add(q)
    return ng


def set_reflect_y(g):
    ng = set()
    for r, c in g:
        r = -r
        q = (r, c)
        ng.add(q)
    return ng


def set_rotate_90(g):
    ng = set()
    for p in g:
        q = rotate90(p)
        ng.add(q)
    return ng


def set_dihedral_arrangements(g, sz):
    """Generator for the 8 arrangements of a square grid
    returns a triple a,b,grid where a is the number of rotations and b reflections"""
    # Rotate 4 times
    # Reflect and rotate 4 times again
    sg = g
    sz -= 1
    for a in range(4):
        yield a, 0, sg
        sg = set_rotate_90(sg)
        sg = set_translate(sg, (sz, 0))

    sg = set_reflect_y(sg)
    sg = set_translate(sg, (sz, 0))
    for a in range(4):
        yield a, 1, sg
        sg = set_rotate_90(sg)
        sg = set_translate(sg, (sz, 0))


#
# dict grid utils
#


def print_dict_grid_values(g, cell_width=5, none_char="", limits=None, headings=True):
    """Visualise a dict grid"""
    min_r, min_c, max_r, max_c = get_grid_limits(g)
    if limits is not None:
        min_r = max(min_r, limits[0])
        min_c = max(min_c, limits[1])
        max_r = min(max_r, limits[2])
        max_c = min(max_c, limits[3])
    print()
    print(f"Rows: {min_r} to {max_r} ,  Columns: {min_c} to {max_c}")
    print()
    row = ""
    if headings:
        row = (" " * cell_width) + "| "
        for c in range(min_c, max_c + 1):
            vs = str(c)
            row += vs.ljust(cell_width)
        print(row)
        row = "-" * len(row)
        print(row)

    for r in range(min_r, max_r + 1):
        row = ""
        if headings:
            row = str(r).ljust(cell_width) + "| "
        for c in range(min_c, max_c + 1):
            vs = str(g.get((r, c), none_char))
            row += vs.ljust(cell_width)
        print(row)


def spiral_out(centre=(0, 0), direction=0):
    """Generator for points on a spiral starting at a centre
    initial heading Right,East,(0,1)"""
    yield centre

    pos = centre
    d = direction

    pos = tuple(map(add, pos, rotations[direction]))
    yield pos
    d += 1

    # now turn when pos on a diagonal
    while True:
        d %= 4
        pos = tuple(map(add, pos, rotations[d]))
        yield pos
        if abs(pos[0]) == abs(pos[1]):
            if d == direction:
                pos = tuple(map(add, pos, rotations[d]))
                yield pos
            d += 1


def spiral_location(n, base=0):
    """Return the row,column for a given value"""
    n += 1 - base
    k = ceil((sqrt(n) - 1) / 2)
    t = 2 * k + 1
    m = t**2
    t = t - 1

    if n >= m - t:
        return k, k - (m - n)
    else:
        m = m - t

    if n >= m - t:
        return k - (m - n), -k
    else:
        m = m - t

    if n >= m - t:
        return -k, -k + (m - n)
    else:
        return (m - n - t) - k, k


def spiral_value(row, col, base=0):
    """Return the value for a row,column"""
    # main code starts downward, so we transform 90 CW
    # to compensate for the visual 90 ACW
    col, row = -row, col
    if abs(col) >= abs(row):
        idx = 4 * col * col - col - row
        if col < row:
            idx -= 2 * (col - row)
    else:
        idx = 4 * row * row - col - row
        if col < row:
            idx += 2 * (col - row)

    return idx + base


def cantor_zigzag(col_first=True):
    """Generator for points on the zig zag diagonal"""
    r, c = 0, 0
    inc_col = col_first
    yield (r, c)
    while True:
        if inc_col and r == 0 or not inc_col and c == 0:
            if inc_col:
                c += 1
            else:
                r += 1

            inc_col = not inc_col
        else:
            if inc_col:
                r -= 1
                c += 1
            else:
                r += 1
                c -= 1

        yield (r, c)


# d = {p: v for v, p in enumerate(islice(cantor_zigzag(col_first=True), 50))}
# print_dict_grid_values(d, limits=(2, 3, 16, 15))


def cantor_location(idx, col_first=True):
    """Return location of an index in a cantor zigzag"""
    md = int(sqrt(2 * idx))
    t_md = ((md + 1) * md) // 2
    if idx < t_md:
        md -= 1

    r = idx - (md * (md + 1) // 2)
    c = md - r
    if md % 2 == 0:
        r, c = c, r

    if not col_first:
        r, c = c, r

    return r, c


def cantor_value(row, col, col_first=True):
    """Return the index of a cantor zigzag location"""
    md = manhattan((row, col))
    base = md * (md + 1) // 2
    parity = 1
    if col_first:
        parity = 0
    if md % 2 == parity:
        idx = base + col
    else:
        idx = base + row
    return idx
