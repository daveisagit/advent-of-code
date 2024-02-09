"""Useful things for 2D grids"""

from collections import namedtuple

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


def manhattan(p):
    """Return the manhattan distance"""
    return abs(p[0]) + abs(p[1])
