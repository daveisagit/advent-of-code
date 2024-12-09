"""Advent of code 2024
--- Day 9: Disk Fragmenter ---
"""

from itertools import pairwise
from common.linked_list import Node, insert_after_node, remove_node, traverse_from_node

from common.aoc import (
    aoc_part,
    get_filename,
    file_to_string,
)


def parse_data(raw_data):
    """Parse the input"""
    dsk = []
    id = 0
    for i, ch in enumerate(raw_data):
        v = int(ch)
        if i % 2 == 1:
            for _ in range(v):
                dsk.append(None)
            continue
        for _ in range(v):
            dsk.append(id)
        id += 1
    return dsk


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    # left and right pointer work toward each other
    rp = len(data) - 1
    lp = 0
    while True:
        while data[lp] is not None and lp < rp:
            lp += 1
        while data[rp] is None and lp < rp:
            rp -= 1
        if lp >= rp:
            break
        data[lp] = data[rp]
        data[rp] = None

    t = 0
    for i, v in enumerate(data):
        if v is None:
            break
        t += i * v
    return t


# Struggling attempt left me actually solving
# with a linked list
# took over 1/2 hour though

# @aoc_part
# def solve_part_b(data) -> int:
#     """Solve part B"""
#     start = Node("start")
#     end = Node("end")
#     start.next = end
#     end.prev = start
#     prv = start
#     id = 0
#     for i, ch in enumerate(data):
#         v = int(ch)
#         if i % 2 == 0:
#             n = Node((id, v))
#             id += 1
#             insert_after_node(prv, n)
#             prv = n
#             continue
#         n = Node((None, v))
#         insert_after_node(prv, n)
#         prv = n

#     for last_used in traverse_from_node(end, forward=False):
#         if last_used.data[0] is None:
#             continue

#         if last_used == start:
#             break

#         for next_free in traverse_from_node(start):
#             if next_free.data[0] is not None:
#                 continue

#             cont = False
#             for n in traverse_from_node(next_free):
#                 if n == last_used:
#                     cont = True
#                     break

#             if not cont:
#                 break

#             if next_free.data[1] >= last_used.data[1]:
#                 new_free = Node((None, next_free.data[1] - last_used.data[1]))
#                 new_used = Node(last_used.data)
#                 new_replace = Node((None, last_used.data[1]))
#                 insert_after_node(last_used, new_replace)
#                 insert_after_node(next_free.prev, new_used)
#                 insert_after_node(new_used, new_free)
#                 remove_node(last_used)
#                 remove_node(next_free)
#                 if new_free.data[1] == 0:
#                     remove_node(new_free)

#     p = 0
#     t = 0
#     for n in traverse_from_node(start):
#         if n == end:
#             break
#         for x in range(n.data[1]):
#             if n.data[0] is not None:
#                 t += p * n.data[0]
#             p += 1

#         print(n.data)

#     return t


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""

    def show():
        by_pos = sorted(files.values())
        id_pos = sorted(files.items(), key=lambda x: x[1])
        sz = max(by_pos)[1]
        s = ["."] * sz
        for fi, (a, b) in id_pos:
            for i in range(a, b):
                s[i] = str(fi)
        print("".join(s))

    def move_to(req: int, before: int):
        """Return the position we can move this file to"""
        by_pos = sorted(files.values())
        to_check = [f for f in by_pos if f[0] <= before]
        for a, b in pairwise(to_check):
            if b[0] - a[1] >= req:
                return a[1]
        return None

    # build a dict keyed on file id values being range on the disk
    p = 0
    id = 0
    files = {}
    for i, ch in enumerate(data):
        v = int(ch)
        if i % 2 == 1:
            p += v
            continue

        if i % 2 == 0:
            assert v > 0
            files[id] = (p, p + v)
            id += 1
            p += v

    for fi in range(len(files) - 1, -1, -1):
        f = files[fi]
        space_required = f[1] - f[0]
        new_p = move_to(space_required, f[0])
        if new_p is not None:
            files[fi] = (new_p, new_p + space_required)

    t = 0
    for fi, (a, b) in files.items():
        pass
        for v in range(a, b):
            t += v * fi

    return t


EX_RAW_DATA = file_to_string(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_RAW_DATA)
solve_part_b(MY_RAW_DATA)
