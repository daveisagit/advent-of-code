"""Advent of code 2019
--- Day 25: Cryostasis ---
"""

from collections import defaultdict, deque
from copy import deepcopy
from itertools import pairwise
from common.aoc import aoc_part, file_to_string, get_filename
from common.general import powerset_swap, tok
from common.intcode import IntCode
from common.graph import dijkstra_paths, optimal_route

bad_items = {
    "escape pod",
    "giant electromagnet",
    "infinite loop",
    "photons",
    "molten lava",
}


def parse_output(out):
    """Return the room, description, doors and items"""
    listing_doors = False
    listing_items = False
    is_the_end = False
    doors = []
    items = []
    room = None
    desc = None
    for line in out:
        if room and not desc:
            desc = line
        if listing_doors:
            if not line:
                listing_doors = False
                continue
            doors.append(line[2:])
        if listing_items:
            if not line:
                listing_items = False
                continue
            items.append(line[2:])
        if line[:2] == "==":
            room = line[3:-3]
        if line.startswith("Doors here lead"):
            listing_doors = True
        if line.startswith("Items here"):
            listing_items = True
        if line.startswith("A loud, robotic voice says"):
            is_the_end = True
            break

    return room, desc, doors, items, is_the_end


def auto_explore(data):
    """Search the place using multiple ics, collecting details
    returning rooms, maps and items/location"""
    ic = IntCode(data)
    bfs = deque()
    rooms = {}
    all_items = defaultdict(set)
    gph = defaultdict(dict)
    out = parse_output(ic.go_ascii([]))
    start = out[0]
    end = None

    bfs.append((ic, out))

    while bfs:
        ic, out = bfs.popleft()
        room, desc, doors, items, is_the_end = out
        if room in rooms:
            continue

        if is_the_end:
            end = room
        rooms[room] = (desc, items)
        for itm in items:
            if itm in bad_items:
                continue
            all_items[room].add(itm)

        for door in doors:
            nic = deepcopy(ic)
            out = parse_output(nic.go_ascii([door]))
            new_room, *_ = out
            bfs.append((nic, out))
            gph[room][new_room] = {"d": 1, "nav": door}

    return rooms, gph, all_items, start, end


def plan_route(gph, rooms_with_items, start, end):
    """Return the best route of rooms to visit to get all the items"""
    rooms_to_visit = set(rooms_with_items)
    _, path = optimal_route(gph, rooms_to_visit, start=start, end=end, weight_attr="d")
    return path


def go_to(ic, cur, room, gph):
    """Go to a given room"""
    _, route = dijkstra_paths(gph, cur, room, weight_attr="d")
    inputs = []
    for u, v in pairwise(route):
        d = gph[u][v]["nav"]
        inputs.append(d)
    out = ic.go_ascii(inputs)
    return out


def collect_items(ic, cur, route, items, gph):
    """Collect all the things"""
    take_out = []
    for r in route:
        go_to(ic, cur, r, gph)
        cur = r
        if r in items:
            itm = list(items[r])[0]
            out = ic.go_ascii([f"take {itm}"])
            take_out.extend(out)
    return take_out, cur


def try_item_combos(ic, items):
    """Try carrying all the possible combos to get the weight right"""

    def combo_correct(out):
        room = True
        for line in out:
            if "ejected back" in line:
                return False
        return room

    s = set()
    for i_set in items.values():
        s.update(i_set)
    items = s

    items_idx = list(reversed(list(items)))
    i_cnt = len(items)
    for idx in powerset_swap(i_cnt):
        c = items_idx[idx]
        if c in items:
            items.remove(c)
            out = ic.go_ascii([f"drop {c}"])
        else:
            items.add(c)
            out = ic.go_ascii([f"take {c}"])

        out = ic.go_ascii(["south"])

        if combo_correct(out):
            out = [l for l in out if l]
            ll = out[-1]
            out.append(f"Combination: {items}")
            for t in tok(ll):
                if t.isdigit():
                    pwd = int(t)
            break

    return out, pwd


def manual_explorer(data):
    """Play the game"""

    rooms, gph, rooms_with_items, start, end = auto_explore(data)
    route = plan_route(gph, rooms_with_items, start, end)
    cur = start

    ic = IntCode(data)
    out = ic.go_ascii([])
    while True:

        for line in out:
            print(line)
        out.clear()

        i = input()

        if i == "q":
            break

        if i == "collect":
            out, cur = collect_items(ic, cur, route, rooms_with_items, gph)
            continue

        if i == "combos":
            out, pwd = try_item_combos(ic, rooms_with_items)
            out.append(f"Password {pwd}")
            continue

        if i == "solve":
            out, cur = collect_items(ic, cur, route, rooms_with_items, gph)
            out, pwd = try_item_combos(ic, rooms_with_items)
            out.append(f"Password {pwd}")
            continue

        if i in rooms:
            out = go_to(ic, cur, i, gph)
            cur = i
            continue

        out = ic.go_ascii([i])


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    _, gph, rooms_with_items, start, end = auto_explore(data)
    route = plan_route(gph, rooms_with_items, start, end)
    cur = start
    ic = IntCode(data)
    collect_items(ic, cur, route, rooms_with_items, gph)
    _, pwd = try_item_combos(ic, rooms_with_items)
    return pwd


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    return len(data)


MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))

# manual_explorer(MY_RAW_DATA)
solve_part_a(MY_RAW_DATA)
