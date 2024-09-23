"""
Compositions:
Split n into k groups, each group can have from 0-n but the sum of them all is always n

Strong Compositions:
A composition but with no zero values
e.g. a strong composition of 5 into 3 groups
[1, 1, 3], [1, 2, 2], [1, 3, 1], [2, 1, 2], [2, 2, 1], [3, 1, 1]
"""

# from collections import defaultdict
# from itertools import combinations_with_replacement


def compositions(n, k):
    """Generator for compositions"""
    if n < 0 or k < 0:
        return
    elif k == 0:
        # the empty sum, by convention, is zero, so only return something if
        # n is zero
        if n == 0:
            yield []
        return
    elif k == 1:
        yield [n]
        return
    else:
        for i in range(0, n + 1):
            for comp in compositions(n - i, k - 1):
                yield [i] + comp


def strong_compositions(n, k):
    """No zeros"""
    for c in compositions(n, k):
        if 0 not in c:
            yield c


# d1 = list(combinations_with_replacement(range(1, 12), 2))
# print(len(d1))
# d2 = list(combinations_with_replacement(range(1, 12), 18))
# print(len(d2))


# two_dice = [0, 0, 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]


# def convolution(a, b):
#     r = [0] * 13
#     for x in a:
#         for y in b:
#             z = x + y
#             if z > 12:
#                 return None
#             r[z] += 1
#             if r[z] > two_dice[z]:
#                 return None
#     if r == two_dice:
#         return True
#     return False


# for a in d1:
#     for b in d2:
#         if convolution(a, b):
#             print(a, b)

# print("fd")
