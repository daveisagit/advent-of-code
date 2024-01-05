"""Useful things for 2D grids"""

from collections import namedtuple

directions = {
    "^": (-1, 0),
    "v": (1, 0),
    "<": (0, -1),
    ">": (0, 1),
}

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
    min_x = min(point[0] for point in point_tuples)
    max_x = max(point[0] for point in point_tuples)
    min_y = min(point[1] for point in point_tuples)
    max_y = max(point[1] for point in point_tuples)
    return min_x, min_y, max_x, max_y
