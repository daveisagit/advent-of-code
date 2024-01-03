"""Useful things for 2D grids"""

from collections import namedtuple


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
