"""Advent of code 2019
--- Day 17: Set and Forget ---
"""

from operator import add
from common.aoc import aoc_part, file_to_string, get_filename
from common.general import find_sublists
from common.intcode import IntCode
from common.grid_2d import directions, rotations


def print_layout(asc):
    """Return the ASCII layout"""
    txt = ""
    for a in asc:
        if a == 10:
            print(txt)
            txt = ""
            continue
        txt += chr(a)


def get_scaffold(data):
    """Return the scaffold as tuples"""
    ic = IntCode(data)
    o = ic.run()
    arrows = {ord(a) for a in directions}
    r = 0
    c = 0
    scaffold = set()
    start_pos = None
    start_dv = None

    for a in o:
        if a in arrows:
            start_pos = (r, c)
            start_dv = directions[chr(a)]
        if a == 35:
            scaffold.add((r, c))
        if a == 10:
            r += 1
            c = 0
            continue
        c += 1

    print_layout(o)
    return scaffold, start_pos, start_dv, data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    scaffold, _, _, _ = data
    total = 0
    for pos in scaffold:
        cnt = 0
        for d in directions.values():
            nxt = tuple(map(add, d, pos))
            if nxt in scaffold:
                cnt += 1
        if cnt == 4:
            total += pos[0] * pos[1]

    return total


def get_route_log(data) -> int:
    """List of turns and distances from start to finish"""

    def on_scaffold(p, d):
        d = rotations[d]
        t = tuple(map(add, d, p))
        if t in scaffold:
            return t
        return None

    def get_new_direction():
        ndi = (di + 1) % 4
        if on_scaffold(pos, ndi):
            return "L", ndi
        ndi = (di - 1) % 4
        if on_scaffold(pos, ndi):
            return "R", ndi
        return None, None

    scaffold, start_pos, start_dv, _ = data
    di = rotations.index(start_dv)
    pos = start_pos
    route_log = []
    cur_dist = 0
    while True:
        nxt = on_scaffold(pos, di)
        if nxt:
            cur_dist += 1
            pos = nxt
            continue
        turn, ndi = get_new_direction()
        if turn:
            if cur_dist > 0:
                route_log.append(cur_dist)
                cur_dist = 0
            route_log.append(turn)
            di = ndi
            continue

        route_log.append(cur_dist)
        break

    return route_log


def get_functions_from_manual_inspection():
    """From manual inspection of the route log"""
    a = "L,6,R,12,R,8"
    b = "R,8,R,12,L,12"
    c = "R,12,L,12,L,4,L,4"
    m = "A,B,B,A,C,A,C,A,C,B"
    return m, {"A": a, "B": b, "C": c}


def get_functions(route_log):
    """Find the functions and main"""
    f_names = "ABC"
    tl = route_log.copy()
    sl = find_sublists(route_log, 3, min_size=4, max_size=10)
    m = []
    while tl:
        for i, l in enumerate(sl):
            if tl[: len(l)] == l:
                fn = f_names[i]
                m.append(fn)
                tl = tl[len(l) :]
                break
    m = ",".join(m)
    fns = {f_names[i]: ",".join(str(c) for c in l) for i, l in enumerate(sl)}
    return m, fns


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    _, _, _, raw = data
    route_log = get_route_log(data)
    pgm_2 = ",".join([str(c) for c in route_log])

    # m, fn = get_functions_from_manual_inspection()
    m, fn = get_functions(route_log)
    mr = m.split(",")
    pgm_1 = []
    for f in mr:
        pgm_1.append(fn[f])
    pgm_1 = ",".join(pgm_1)

    assert pgm_1 == pgm_2
    print(pgm_1)
    print(pgm_2)

    # Enter the commands
    inputs = []
    prompt = [ord(c) for c in m]
    prompt.append(10)
    inputs.extend(prompt)

    for f in "ABC":
        s = fn[f]
        prompt = [ord(c) for c in s]
        prompt.append(10)
        inputs.extend(prompt)

    inputs.extend([ord("n"), 10])

    ic = IntCode(raw)
    ic.code[0] = 2
    o = ic.run(inputs)

    print("".join([chr(c) for c in ic.output[:-1]]))

    return o[-1]


MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = get_scaffold(MY_RAW_DATA)

solve_part_a(MY_DATA)
solve_part_b(MY_DATA)
