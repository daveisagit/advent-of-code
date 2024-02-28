"""Multi-dimensional blocks"""

from itertools import pairwise


def combine_blocks(a: list, b: list) -> list:
    """A block is a list of dimension pairs (Bx,B'x), (By,B'y), (Bz,B'z)
    where B and B' are the opposite corners. Each pair is like a side of a block.
    The return is a set of blocks which represent the resulting possible workspace
    The client of this function can then determine the relevance of each
    within its own context.
    """
    result = []
    grid_markers = [sorted(set(list(sides[0]) + list(sides[1]))) for sides in zip(a, b)]
    dimensions = len(grid_markers)

    def iterate_dimension(other_sides: list):
        cur_depth = len(other_sides)
        markers = grid_markers[cur_depth]
        for side in pairwise(markers):
            new_list_of_sides = other_sides + [side]
            if cur_depth < dimensions - 1:
                iterate_dimension(new_list_of_sides)
                continue
            result.append(tuple(new_list_of_sides))

    iterate_dimension([])

    return result


def intersection_block(a: list, b: list) -> list:
    """Intersection: of the workspace which new sub blocks are in a and b
    Should be 1 or 0 in theory?"""
    result = []
    for c in combine_blocks(a, b):
        c_inside_a = all(
            a_side[0] <= c_side[0] and c_side[1] <= a_side[1]
            for a_side, c_side in zip(a, c)
        )
        c_inside_b = all(
            b_side[0] <= c_side[0] and c_side[1] <= b_side[1]
            for b_side, c_side in zip(b, c)
        )
        if c_inside_a and c_inside_b:
            result.append(c)
    return result


def test_intersection_block():
    """Test intersection_block"""
    a = ((1, 5), (3, 7))  # 1 @ 1,3: 4x4
    b = ((3, 7), (1, 5))  # 2 @ 3,1: 4x4
    c = ((5, 7), (5, 7))  # 3 @ 5,5: 2x2
    assert intersection_block(a, b) == [((3, 5), (3, 5))]
    assert intersection_block(a, c) == []
    assert intersection_block(b, c) == []


test_intersection_block()
