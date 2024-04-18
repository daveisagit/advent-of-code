"""
Compositions:
Split n into k groups, each group can have from 0-n but the sum of them all is always n

Strong Compositions:
A composition but with no zero values
e.g. a strong composition of 5 into 3 groups
[1, 1, 3], [1, 2, 2], [1, 3, 1], [2, 1, 2], [2, 2, 1], [3, 1, 1]
"""


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
