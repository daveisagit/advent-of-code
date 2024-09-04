"""Lattice over n dimensions"""

from collections import defaultdict
from operator import add, sub
from common.general import powerset


def distance_sq(p):
    return sum(x**2 for x in p)


def manhattan(p, rel=None):
    """Return the manhattan distance"""
    if rel is None:
        rel = [0] * len(p)
    p = tuple(map(sub, p, rel))
    return sum(abs(x) for x in p)


def multirange(d, m):
    """Return all lattice points in the m sized hypercube of d dimensions"""
    for i in range(m**d):
        x = i
        r = []
        for _ in range(d):
            x, rem = divmod(x, m)
            r.append(rem)
        yield tuple(r)[::-1]


def generate_Nn(n=2, limit=None, dist_metric="manhattan"):
    """Generator for a lattice in n-dimensions"""
    ymax = defaultdict(int)  # unknown keys are mapped to 0
    d = 0
    while limit is None or d <= limit:
        to_yield = []
        while True:
            batch = []
            for x in multirange((n - 1), d + 1):
                y = ymax[x]
                pt = x + (y,)
                if "squ" in dist_metric:
                    if distance_sq(pt) <= d**2:
                        batch.append(pt)
                        ymax[x] += 1
                else:
                    if manhattan(pt) <= d:
                        batch.append(pt)
                        ymax[x] += 1
            if not batch:
                break
            to_yield += batch
        if "squ" in dist_metric:
            to_yield.sort(key=distance_sq)
        else:
            to_yield.sort(key=manhattan)
        for p in to_yield:
            yield p
        d += 1


def generate_Zn(n=2, limit=None, origin=None, dist_metric="manhattan"):
    """Generator for integer lattice
    limit using the distance metric
    i.e. manhattan distance or square"""
    if origin is None:
        origin = [0] * n
    for p in generate_Nn(n=n, limit=limit, dist_metric=dist_metric):
        for s in powerset(range(n)):
            t = list(p)
            no_zeros = True
            for i in s:
                if t[i] == 0:
                    no_zeros = False
                    break
                t[i] = -t[i]
            if no_zeros:
                yield tuple(map(add, t, origin))


# for x in generate_Zn(n=2, limit=3, origin=(10, 10)):
#     print(x)

# print(len(list(generate_Zn(n=2, limit=3))))

# print(sorted(list(generate_Zn(n=3, limit=3))))

# print(sorted(list(generate_Zn(n=4, limit=2))))

# print(list(multirange(3, 3)))
