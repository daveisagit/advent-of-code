"""For solving stuff on hex grid using cube coordinates"""

# assuming an East/West orientation - best suited for drawing in text
#       @ @
#      @ . @
#       @ @


from collections import defaultdict
from operator import add, sub
from common.grid_2d import print_single_char_dict_grid


compass_EW = [
    "E",
    "NE",
    "NW",
    "W",
    "SW",
    "SE",
]

# mentally rotated 30 ACW to get North/South
compass_SN = [
    "SE",
    "NE",
    "N",
    "NW",
    "SW",
    "S",
]

# zip to the hectors
hectors = [
    (1, 0, -1),
    (1, -1, 0),
    (0, -1, 1),
    (-1, 0, 1),
    (-1, 1, 0),
    (0, 1, -1),
]

compass = {c: p for c, p in zip(compass_EW, hectors)}


def flip_point(p):
    """Reflect a point over vertical centre line through origin
    If NS then over the NE/SW line"""
    return p[2], p[1], p[0]


def flip_points(ps):
    """Reflect a point over vertical centre line through origin
    If NS then over the NE/SW line"""
    return [flip_point(p) for p in ps]


def rotate_point(p):
    """Rotate ACW 60 - shift coordinates right and multiply -1"""
    return tuple(-p[(i - 1) % 3] for i in range(3))


def rotate_points(ps):
    """Rotate ACW 60 - shift coordinates right and multiply -1"""
    return [rotate_point(p) for p in ps]


def generate_dihedral_symmetries(points):
    """Generator for the dihedral symmetries
    Yields the new set of points and the change to a reference point"""

    def generate_rotations(points):
        for _ in range(6):
            yield points
            points = rotate_points(points)

    yield from generate_rotations(points)
    points = flip_points(points)
    yield from generate_rotations(points)


def scalar_multiply(v, s):
    return tuple(x * s for x in v)


def translate_points(points, vector):
    """Translate all point by the given vector"""
    # tuple(map(add, p, vector))
    return tuple(tuple(map(add, p, vector)) for p in points)


def point_to_doubled(p):
    return p[1], p[0] - p[2]


def pattern_to_doubled(pt):
    return [point_to_doubled(p) for p in pt]


def point_from_doubled(d):
    return (d[1] - d[0]) // 2, d[0], (-d[1] - d[0]) // 2


def pattern_from_doubled(pt):
    return [point_from_doubled(p) for p in pt]


def manhattan(a, b=(0, 0, 0)):
    c = tuple(map(sub, a, b))
    return sum([abs(x) for x in c]) // 2


def generate_circle(n, origin=(0, 0, 0)):
    for q in range(-n, n + 1):
        for r in range(max(-n, -q - n), min(n, -q + n) + 1):
            s = -q - r
            p = q, r, s
            if manhattan(p) < n:
                continue
            yield tuple(map(add, p, origin))


def generate_circle_filled(n, origin=(0, 0, 0)):
    for q in range(-n, n + 1):
        for r in range(max(-n, -q - n), min(n, -q + n) + 1):
            s = -q - r
            p = q, r, s
            yield tuple(map(add, p, origin))


def neighbours(p):
    for v in hectors:
        yield tuple(map(add, p, v))


def normalise_position(points):
    """Translate the pattern to the top left in a consistent fashion
    This will allow us to identify a unique pattern by its coordinate set"""
    min_r = min(p[1] for p in points)
    v1 = scalar_multiply(hectors[1], min_r)
    points = translate_points(points, v1)

    min_c = min(p[0] for p in points)
    v2 = scalar_multiply(hectors[3], min_c)
    points = translate_points(points, v2)
    return points


def get_graph(points) -> dict:
    """Return a graph dict of the points"""
    gph = defaultdict(dict)
    for u in points:
        for v in neighbours(u):
            if v in points:
                gph[u][v] = 1
                gph[v][u] = 1
    return gph


def test():

    ps = {p: str(i) for i, p in enumerate(pattern_to_doubled(hectors))}
    print_single_char_dict_grid(ps)

    test_pattern = hectors + [
        (2, 0, -2),
        (2, 1, -3),
    ]

    for tp in generate_dihedral_symmetries(test_pattern):
        ps = {p: "@" for p in pattern_to_doubled(tp)}
        print_single_char_dict_grid(ps)
    print()

    for p in test_pattern:
        print(p, manhattan(p))

    for i, p in enumerate(hectors):
        print(i, manhattan(p, (2, 1, -3)))

    tp = list(generate_circle_filled(2))
    ps = {p: "@" for p in pattern_to_doubled(tp)}
    print_single_char_dict_grid(ps)

    tp = list(generate_circle(3, origin=(-5, 0, 5)))
    ps = {p: "@" for p in pattern_to_doubled(tp)}
    print_single_char_dict_grid(ps)

    print(compass)


test()
