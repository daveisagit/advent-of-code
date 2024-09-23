"""Mostly 2D matrices functions"""


def mtx_print(m):
    """A quick visual"""
    for row in m:
        print(row)


def mtx_mul(a, b):
    """Return ab and allow for b as a scalar"""
    if isinstance(b, int):
        return [[x * b for x in row] for row in a]
    if len(a[0]) != len(b):
        raise ValueError("Incompatible matrices for multiplication")
    rows_a = len(a)
    cols_b = len(b[0])
    result = [[0] * cols_b for _ in range(rows_a)]
    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(len(a)):
                result[i][j] += a[i][k] * b[k][j]
    return result


def mtx_transpose(m):
    return list(map(list, zip(*m)))


def mtx_get_minor(m, i, j):
    return [row[:j] + row[j + 1 :] for row in (m[:i] + m[i + 1 :])]


def mtx_determinant(m):
    """Return the determinant"""
    # base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1) ** c) * m[0][c] * mtx_determinant(mtx_get_minor(m, 0, c))
    return determinant


def mtx_inverse(m):
    """Return the inverse as a tuple (det,inv)"""
    determinant = mtx_determinant(m)
    # special case for 2x2 matrix:
    if len(m) == 2:
        return determinant, [[m[1][1], -1 * m[0][1]], [-1 * m[1][0], m[0][0]]]

    # find matrix of cofactors
    cofactors = []
    for r in range(len(m)):
        cofactor_row = []
        for c in range(len(m)):
            minor = mtx_get_minor(m, r, c)
            cofactor_row.append(((-1) ** (r + c)) * mtx_determinant(minor))
        cofactors.append(cofactor_row)
    cofactors = mtx_transpose(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]
    return determinant, cofactors


def mtx_solve(m, v, expect_integer=True):
    """Given m,v represent a system of linear equations return a solution
    m: [][]
    v: tuple()
    """
    v = mtx_transpose([v])
    det, inv = mtx_inverse(m)
    if det == 0:
        raise ValueError("No unique solution, determinant not zero")
    r = mtx_mul(inv, v)
    r = tuple(mtx_transpose(r)[0])
    if expect_integer:
        if all(x % det == 0 for x in r):
            r = tuple(x // det for x in r)
            return r
        else:
            raise RuntimeError("Expected integer result")
    return det, r


def quadratic_from_3_points(x, y):
    """Return quadratic coefficients a,b,c for the 3 points
    using Lagrange polynomial interpolation"""
    m = []
    for i in range(3):
        row = [x[i] ** 2, x[i], 1]
        m.append(row)
    r = mtx_solve(m, y)
    return r


def poly_from_points(x, y, expect_integer=True):
    """Return polynomial coefficients a,b,c for the curve through points
    using Lagrange polynomial interpolation.
    Returns a tuple ( y-coefficient, (x-coefficients,))
    If starting with a points list i.e. points = ((1, 4), (2, 7), (3, 12))
    Then (x,y) = [t for t in zip(*points)]
    """
    mtx = []
    assert len(x) == len(y)
    terms = len(x)
    for i in range(terms):
        row = [x[i] ** e for e in range(terms)]
        mtx.append(row)
    return mtx_solve(mtx, y, expect_integer=expect_integer)


def poly_value(poly, x):
    """Return the value f(x) given f() and x
    fx expressed as (y,(x,))
    We assert for an integer answer"""
    yc, xcs = poly
    terms = len(xcs)
    x_sum = sum(xcs[t] * x**t for t in range(terms))
    assert x_sum % yc == 0
    return x_sum // yc


def test_inv():
    m = [
        [4, 3, 7],
        [9, 8, 1],
        [2, 6, 5],
    ]
    det, i = mtx_inverse(m)
    assert det == 273
    assert i == [
        [34, 27, -53],
        [-43, 6, 59],
        [38, -18, 5],
    ]

    a = [
        [1],
        [2],
        [3],
    ]

    b = [
        [31],
        [28],
        [29],
    ]

    r = mtx_mul(i, b)
    r2 = mtx_mul(a, det)
    assert r == r2

    d, r = mtx_solve(m, (31, 28, 29), expect_integer=False)
    assert d == 273
    assert r == (273, 546, 819)


def test_quadratic_from_3_points():
    points = ((1, 4), (2, 7), (3, 12))
    arr = [t for t in zip(*points)]
    x = arr[0]
    y = arr[1]
    cof = quadratic_from_3_points(x, y)
    assert cof == (1, 0, 3)


test_quadratic_from_3_points()
