"""Advent of code 2023
--- Day 24: Never Tell Me The Odds ---

P = position 
V = velocity

In the XY plane
m = Vy / Vx
y = mx + c
Py = (Vy/Vx)Px + c
c = Py - (Vy/Vx)Px

y = (Vy/Vx)x + Py - (Vy/Vx)Px

yVx = xVy + VxPy - PxVy

So expressing the trajectory P,V as ax + by = c in the XY-plane
PxVy - VxPy = xVy - yVx

Giving values for a,b,c 
a = Vy
b = -Vx
c = PxVy - PyVx

which suits matrix based linear algebra for finding 
the intersection points
"""

from itertools import combinations
from operator import sub
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok
from common.grid_2d import generate_Z2
from common.linear_algebra import mtx_solve


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        arr = tok(line, "@")
        p = tuple(int(x) for x in tok(arr[0], ","))
        v = tuple(int(x) for x in tok(arr[1], ","))
        data.append((p, v))
    return data


@aoc_part
def solve_part_a(data, l_bound=7, u_bound=27) -> int:
    """Solve part A"""
    xy_data = [(p[:-1], v[:-1]) for p, v in data]
    # expressed as ax + by = c in tuple (a,b,c)
    # a = Vy = v[1]
    # b = -Vx = -v[0]
    # c = PxVy - PyVx = (p[0] * v[1] - p[1] * v[0]
    eq_data = [(v[1], -v[0], (p[0] * v[1] - p[1] * v[0])) for p, v in xy_data]
    cnt = 0

    # look at every pairing combo
    for ai, bi in combinations(range(len(eq_data)), 2):

        # a,b as given in the position,velocity form
        pv_a = xy_data[ai]
        pv_b = xy_data[bi]

        # a,b as their path in the XY-plane
        eq_a = eq_data[ai]
        eq_b = eq_data[bi]

        # find the intersection at r
        m = [eq_a[:-1], eq_b[:-1]]
        c = eq_a[2], eq_b[2]
        try:
            dn, r = mtx_solve(m, c, expect_integer=False)
            r = tuple(x / dn for x in r)
        except ValueError:
            # No solution i.e. parallel
            continue

        # back in time, the change in position is an opposite sign
        # to the velocity
        if any((r[i] - pv_a[0][i]) * pv_a[1][i] < 0 for i in range(2)):
            continue
        if any((r[i] - pv_b[0][i]) * pv_b[1][i] < 0 for i in range(2)):
            continue

        # inside the test grid limits
        if all(l_bound <= r[i] <= u_bound for i in range(2)):
            cnt += 1

    return cnt


def determine_z_collision(p, v, r, w):
    """Given vectors for a stone and the rock
    return the collision in the z-plane and the time it occurred"""

    # make the ax+by=c form for the 2 bodies
    c_stone = p[0] * v[1] - p[1] * v[0]
    c_rock = r[0] * w[1] - r[1] * w[0]
    c = (c_stone, c_rock)
    m = [
        [v[1], -v[0]],  # a,b for stone
        [w[1], -w[0]],  # a,b for the rock
    ]
    # find collision point in the XY-plane
    collision = mtx_solve(m, c)

    # get the time taken for the stone to collide with the rock
    t_x = (collision[0] - p[0]) // v[0]
    t_y = (collision[1] - p[1]) // v[1]
    assert t_x == t_y
    t = t_x

    p_z = p[2]
    v_z = v[2]
    collision_z = p_z + v_z * t
    return collision_z, t


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B
    Strategy:
    Work relative to the thrown rock (position = R, velocity = W), so each hailstone has a
    new relative velocity (V').
    V' = V - W

    Since the rock is not moving from this relative viewpoint
    every hailstone will collide with the rock at R (at some point in time).

    Use the technique from part A to just look at the XY-plane and the path
    traced across it by the hailstone.

    All hailstones will have their XY-plane paths intersecting at R.

    We know how to generate the XY path equation in ax+by=c form
    xV'y - yV'x = PxV'y - V'xPy
    =>  a = V'y , b = -V'x , c = PxV'y - PyV'x

    Now V' is unknown (based on W) but if we did know it, we could pick any 2
    hailstones and derive where the rock was thrown from (R) by solving the simultaneous
    linear paths for each stone.

    If we have the wrong value for W then not all resulting solutions for R would be the same.
    Maybe go so far as to say any 2 different pairs would have different solutions for R.

    So we can take the approach of testing possible values for W to see how they affect the
    value for R on separate pairs of hailstones.

    For example, given value for W, we can see where hailstones a,b intersect, say at R1 and
    also where hailstones a,c intersect, say at R2.
    If R1 = R2 then we must be on the right trajectory to hit all 3 hailstones.
    Since this is the only path to satisfy hailstones a,b,c by definition of the problem
    it must also pass through every other hailstone too.

    This will give us the rock's position and velocity in the x,y dimensions

    We now revert back to real world (not relative) to find the collision points
    with 2 stones in the XY-plane. We can then determine the z-coordinate of these
    2 collision points using the time taken.

    Having 2 z-coordinates at 2 times will give us a rock velocity in the z-plane
    so we can then determine it starting z-coordinate

    """
    xy_data = [(p[:-1], v[:-1]) for p, v in data]

    for w in generate_Z2():

        # Using the first 3 stones in the list 0,1,2
        # get their position and velocity vectors
        p0 = list(xy_data[0][0])
        v0 = list(xy_data[0][1])
        p1 = list(xy_data[1][0])
        v1 = list(xy_data[1][1])
        p2 = list(xy_data[2][0])
        v2 = list(xy_data[2][1])

        # here v_ represents V' the relative velocity of each hailstone
        v_0 = list(map(sub, v0, w))
        v_1 = list(map(sub, v1, w))
        v_2 = list(map(sub, v2, w))

        # in the XY-plane get the ax+by=c form
        # a = V'y , b = -V'x , c = PxV'y - PyV'x

        # values for the c_vector
        c0 = p0[0] * v_0[1] - p0[1] * v_0[0]
        c1 = p1[0] * v_1[1] - p1[1] * v_1[0]
        c2 = p2[0] * v_2[1] - p2[1] * v_2[0]

        # Find the rock position for the 0,1 pair (r1)
        m1 = [
            [v_0[1], -v_0[0]],  # a,b for 0
            [v_1[1], -v_1[0]],  # a,b for 1
        ]
        c_vector1 = (c0, c1)
        try:
            r1 = mtx_solve(m1, c_vector1)
        except RuntimeError:
            # ignore non integer results
            continue
        except ValueError:
            # No solution i.e. parallel
            continue

        # Find the rock position for the 0,2 pair (r2)
        m2 = [
            [v_0[1], -v_0[0]],  # a,b for 0
            [v_2[1], -v_2[0]],  # a,b for 2
        ]
        c_vector2 = (c0, c2)
        try:
            r2 = mtx_solve(m2, c_vector2)
        except RuntimeError:
            # ignore non integer results
            continue
        except ValueError:
            # No solution i.e. parallel
            continue

        # if they match then this rock velocity is the one!
        if r1 == r2:
            # Now we need the z-coordinate of the rock's initial position

            # If we know 2 collision points and when they happened we can
            # figure z-plane velocity and hence z-position of the rock

            # Collision with stone 0
            p = data[0][0]
            v = data[0][1]
            collision0_z, t0 = determine_z_collision(p, v, r1, w)

            # Collision with stone 1
            p = data[1][0]
            v = data[1][1]
            collision1_z, t1 = determine_z_collision(p, v, r1, w)

            # Now we can calc the z-velocity for the rock
            rock_vel_z = (collision1_z - collision0_z) // (t1 - t0)

            # working back from the collision with stone 0
            rock_pos_z = collision0_z - t0 * rock_vel_z
            return sum(r1) + rock_pos_z

    return len(data)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA, l_bound=200000000000000, u_bound=400000000000000)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
