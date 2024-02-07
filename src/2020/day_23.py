"""Advent of code 2020
--- Day 23: Crab Cups ---
"""

from common.aoc import aoc_part


def parse_data(raw_data):
    """Parse the input"""
    return [int(i) for i in list(str(raw_data))]


def iterate_a(cups):
    """Current cup is always first"""
    sz = len(cups)
    cur = cups[0]
    rmv = cups[1:4]
    rest = cups[4:]

    nxt = cur
    while True:
        nxt -= 1
        if nxt < 1:
            nxt = sz - 1
        if nxt not in rmv:
            break

    ni = rest.index(nxt)

    new_layout = rest[: ni + 1]
    new_layout.extend(rmv)
    new_layout.extend(rest[ni + 1 :])
    new_layout.append(cur)
    return new_layout


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    data = parse_data(data)
    for _ in range(100):
        data = iterate_a(data)
    idx = data.index(1)
    ans = data[idx + 1 :]
    ans.extend(data[:idx])
    ans = "".join([str(a) for a in ans])
    return ans


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B as a linked list"""

    def iterate(cur):
        """Ooo my those crabs"""

        rmv = []
        r = cur
        for _ in range(3):
            r = cw[r]
            rmv.append(r)

        fr = rmv[0]
        lr = rmv[-1]
        lr2 = cw[lr]

        dst = cur
        while True:
            dst -= 1
            if dst < 1:
                dst = M1
            if dst not in rmv:
                break

        dst2 = cw[dst]

        # remove rmv (joining cur to lr2)
        cw[cur] = lr2
        acw[lr2] = cur

        # add - update pointers for the rmv block
        acw[fr] = dst
        cw[lr] = dst2

        # add - update pointers for dst and dst2
        acw[dst2] = lr
        cw[dst] = fr

        return lr2

    M1 = 1000000
    M11 = M1 + 1
    data = parse_data(data)
    acw = [0] * M11
    cw = [0] * M11
    data = data + list(range(max(data) + 1, M11))
    for i, x in enumerate(data[1:-1]):
        cw_x = data[i + 2]
        cw[x] = cw_x
        acw_x = data[i]
        acw[x] = acw_x

    fx = data[0]
    lx = data[-1]
    cw[fx] = data[1]
    cw[lx] = data[0]

    acw[fx] = data[-1]
    acw[lx] = data[-2]

    cur = 3
    for _ in range(10000000):
        cur = iterate(cur)

    a = cw[1]
    b = cw[a]

    return a * b


EX_DATA = 389125467
MY_DATA = 398254716

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
