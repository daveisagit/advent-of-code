"""A mish-mash of partitioning algorithms best explained as printed examples
Copied into partitions.py as needed by AoC, such as 2015.15
"""

from itertools import combinations_with_replacement as cr


def partition_count(n):
    """
    ways to partition n
    :param n:
    :return:
    """
    parts = [1] + [0] * n
    for t in range(1, n + 1):
        for i, x in enumerate(range(t, n + 1)):
            parts[x] += parts[i]
    return parts[n]


print("partition_count")
print(partition_count(5))


def unique_partitions_of(n):
    """
    ordered partitions of n
    :param n:
    :return:
    """
    answer = set()
    answer.add((n,))
    for x in range(1, n):
        for y in unique_partitions_of(n - x):
            answer.add(tuple(sorted((x,) + y)))
    return answer


print("unique_partitions_of")
print(unique_partitions_of(5))


def partitions_of(n):
    """
    ordered partitions of n
    :param n:
    :return:
    """
    answer = set()
    answer.add((n,))
    for x in range(1, n):
        for y in partitions_of(n - x):
            answer.add(tuple((x,) + y))
    return answer


print("partitions_of")
print(partitions_of(5))


def set_partition(collection):
    if len(collection) == 1:
        yield [collection]
        return

    first = collection[0]
    for smaller in set_partition(collection[1:]):
        # insert `first` in each of the subpartition's subsets
        for n, subset in enumerate(smaller):
            yield smaller[:n] + [[first] + subset] + smaller[n + 1 :]
        # put `first` in its own subset
        yield [[first]] + smaller


print("set_partitions")
something = list(range(100, 105))
for n, p in enumerate(set_partition(something), 1):
    print(n, sorted(p))


def coin_change(n, coins):
    parts = [1] + [0] * n
    for c in coins:
        for i, x in enumerate(range(c, n + 1)):
            parts[x] += parts[i]
    return parts[n]


print("coin_change")
print(coin_change(100, {1, 5, 10, 25, 50, 100}))
print(coin_change(10, {1, 2, 5, 10, 20, 50, 100}))


def constrained_partitions(n, k, min_elem, max_elem):
    """
    partition n into k partitions such each partition is constrained by min/max
    :param n:
    :param k:
    :param min_elem:
    :param max_elem:
    :return:
    """
    allowed = range(max_elem, min_elem - 1, -1)

    def helper(n, k, t):
        if k == 0:
            if n == 0:
                yield t
        elif k == 1:
            if n in allowed:
                yield t + (n,)
        elif min_elem * k <= n <= max_elem * k:
            for v in allowed:
                yield from helper(n - v, k - 1, t + (v,))

    return helper(n, k, ())


print("constrained_partitions: fixed number of partitions")
print("constrained_partitions of 5 into 3 where 0<=p<=3")
for p in constrained_partitions(5, 3, 0, 3):
    print(p)
print("constrained_partitions of 5 into 3 where 1<=p<=5")
for p in constrained_partitions(5, 3, 1, 5):
    print(p)


def all_partitions(n, k):
    """
    Return all possible combinations that add up to n
    i.e. divide n objects in k DISTINCT boxes in all possible ways
    """
    all_part = []
    for div in cr(range(n + 1), k - 1):
        counts = [div[0]]
        for i in range(1, k - 1):
            counts.append(div[i] - div[i - 1])
        counts.append(n - div[-1])
        all_part.append(counts)
    return all_part


print("all_partitions of 5 into 3")
print(all_partitions(5, 3))


def compositions(n, k):
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


print("composition into fixed number of parts")
print(f"compositions of 4 into 4 = {sum([1 for c in compositions(4, 4)])}")
print([c for c in compositions(4, 4)])


def strong_compositions(n, k):
    for c in compositions(n, k):
        if 0 not in c:
            yield c


print("strong composition of 5 into fixed number of parts (no zeros)")
print([c for c in strong_compositions(5, 3)])
