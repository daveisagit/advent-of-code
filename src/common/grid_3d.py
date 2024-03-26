"""Anything 3D"""

from collections import namedtuple

XYZ = namedtuple(
    "XYZ",
    ["x", "y", "z"],
)


def all_90_rotations():
    """Return a list of all the possible 90 degree rotations generated using:
    Roll -> 3x Turn CW -> Roll -> 3x Turn CCW -> Roll -> 3x Turn CW -> Roll -> 3x Turn CCW -> Roll -> 3x Turn CW -> Roll -> 3x Turn CCW
    """

    # roll (x-invariant)
    # z
    # |_y
    roll_map = {
        "+y": "+z",
        "+z": "-y",
        "-y": "-z",
        "-z": "+y",
    }

    # ccw (y-invariant)
    # z
    # |_x
    ccw_map = {
        "+x": "+z",
        "+z": "-x",
        "-x": "-z",
        "-z": "+x",
    }

    # cw (y-invariant)
    # z
    # |_x
    cw_map = {
        "+z": "+x",
        "+x": "-z",
        "-z": "-x",
        "-x": "+z",
    }

    def roll(cur):
        return tuple([roll_map.get(o, o) for o in cur])

    def ccw(cur):
        return tuple([ccw_map.get(o, o) for o in cur])

    def cw(cur):
        return tuple([cw_map.get(o, o) for o in cur])

    all_24 = []
    cur = ("+x", "+y", "+z")
    for roll_index in range(6):
        cur = roll(cur)
        all_24.append(cur)
        for _ in range(3):
            cur = cw(cur) if roll_index % 2 == 0 else ccw(cur)
            all_24.append(cur)

    return all_24


def rotate_a_point(p: XYZ, rot):
    """Given a rotation as listed in all_90_rotations, rotate about origin"""
    new_point = [0] * 3
    for i in range(3):
        v = p[i]
        to_axis = rot[i]
        if to_axis[0] == "-":
            v = -v
        to_axis = to_axis[1]
        to_axis = "xyz".index(to_axis)
        new_point[to_axis] = v
    return tuple(new_point)


def test_rotation():
    """Take the diagonal / across the front face"""
    dg = ((-1, -1, -1), (-1, 1, 1))
    a, b = dg
    dgs = set()
    for r in all_90_rotations():
        a2 = rotate_a_point(a, r)
        b2 = rotate_a_point(b, r)
        dg2 = (a2, b2)
        print(dg2)
        dgs.add(dg2)

    print(len(dgs))


def get_grid_limits(point_tuples):
    """Return the limits of the data"""
    if not point_tuples:
        return 0, 0, 0, 0, 0, 0
    min_x = min(point[0] for point in point_tuples)
    max_x = max(point[0] for point in point_tuples)
    min_y = min(point[1] for point in point_tuples)
    max_y = max(point[1] for point in point_tuples)
    min_z = min(point[2] for point in point_tuples)
    max_z = max(point[2] for point in point_tuples)

    return min_x, min_y, min_z, max_x, max_y, max_z
