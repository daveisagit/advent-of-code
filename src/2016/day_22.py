"""Advent of code 2016
--- Day 22: Grid Computing ---
"""

from copy import deepcopy
from heapq import heappop, heappush
from operator import add
import re
from common.aoc import file_to_list, aoc_part, get_filename
from common.grid_2d import directions, manhattan


def parse_data(raw_data):
    """Parse the input"""
    nodes = {}
    for line in raw_data[2:]:
        rr = re.search(
            r"/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)%", line
        )
        t = [int(x) for x in rr.groups()]
        p = tuple(t[:2])
        d = t[2:]
        nodes[p] = d

    return nodes


@aoc_part
def solve_part_a(nodes) -> int:
    """Solve part A"""
    cnt = 0
    for a, da in nodes.items():
        for b, db in nodes.items():
            if a == b:
                continue
            if da[1] == 0:  # used is empty
                continue
            if da[1] > db[2]:  # used on a is > available on b
                continue
            cnt += 1

    return cnt


@aoc_part
def solve_part_b(nodes) -> int:
    """Solve part B"""
    start = max(n[0] for n in nodes)
    h = []
    seen = set()
    usage = []
    empty = None
    for p, dat in nodes.items():
        dat = tuple(dat[:2])
        usage.append((p, dat))
        if dat[1] == 0:
            empty = p
    usage = tuple(sorted(usage))
    pos = (start, 0)
    md = manhattan(empty, pos)
    state = (pos, md, empty, 0, usage)
    heappush(h, state)

    while h:

        pos, md, empty, steps, usage = heappop(h)
        if (pos, empty) in seen:
            continue
        seen.add((pos, empty))

        if pos == (0, 0):
            return steps

        ws = {p: list(dat) for p, dat in usage}

        for p, dat in usage:

            if dat[1] == 0:
                continue

            for d in directions.values():
                n = tuple(map(add, p, d))

                if n not in ws:
                    continue

                avl = ws[n][0] - ws[n][1]
                if ws[p][1] > avl:
                    continue

                new_usage = deepcopy(ws)
                new_usage[p][1] = 0
                new_usage[n][1] += ws[p][1]
                new_usage = [(p, tuple(dat)) for p, dat in new_usage.items()]
                new_usage = tuple(sorted(new_usage))
                new_pos = pos
                new_empty = empty
                if p == pos:
                    new_pos = n
                if n == empty:
                    new_empty = p
                md = manhattan(new_empty, new_pos)
                new_state = (new_pos, md, new_empty, steps + 1, new_usage)
                heappush(h, new_state)

    return None


@aoc_part
def solve_part_c(nodes) -> int:
    """Solve part B"""
    from_x = max(n[0] for n in nodes)
    # find the empty one dat_1 = used
    # we will move this around as much if not more than the
    # block @ (from_x,0)
    empties = [p for p, dat in nodes.items() if dat[1] == 0]
    assert len(empties) == 1
    empty_pos = empties[0]

    # we will keep state on the used amount in the grid
    # as well as cur_pos & empty_pos
    # used is an immutable rep of usage for the whole grid
    # we dont need to make the rep hash unique so no need to sort
    used = tuple([(p, u) for p, (_, u, _, _) in nodes.items()])

    cur_pos = (from_x, 0)
    md = manhattan(empty_pos, cur_pos)

    # use a min heap to prioritise positions closer to 0,0
    # and within that ones with a closer empty cell

    state = (cur_pos, md, empty_pos, 0, used)
    seen = set()
    h = []
    heappush(h, state)

    while h:

        cur_pos, md, empty_pos, steps, used = heappop(h)

        # dont repeat the same cur_pos, empty_pos
        if (cur_pos, empty_pos) in seen:
            continue
        seen.add((cur_pos, empty_pos))

        if cur_pos == (0, 0):
            return steps

        # make a mutable version of used, working storage (ws)
        ws = {p: u for p, u in used}
        available = nodes[empty_pos][0]

        for d in directions.values():
            n = tuple(map(add, empty_pos, d))

            # ignore off grid
            if n not in ws:
                continue

            # ignore if too large
            if ws[n] > available:
                continue

            new_used = deepcopy(ws)
            new_used[n] = 0
            new_used[empty_pos] = ws[n]
            new_used = tuple([(p, u) for p, u in new_used.items()])

            new_pos = cur_pos
            new_empty = n
            if n == cur_pos:
                new_pos = empty_pos
            md = manhattan(new_empty, new_pos)
            new_state = (new_pos, md, new_empty, steps + 1, new_used)
            heappush(h, new_state)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)

solve_part_c(MY_DATA)
