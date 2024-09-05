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
from common.visuals import visualize_graph


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
        door = gph[u][v]["nav"]
        inputs.append(door)
    out = ic.go_ascii(inputs)
    return out


def get_bad_items(data, gph, start, rooms_with_items):
    """Don't touch!"""
    bad_items = {
        "infinite loop": "Very funny!",
        "giant electromagnet": "The giant electromagnet is stuck to you.  You can't move!!",
    }
    item_room_map = {}
    for room, items in rooms_with_items.items():
        for i in items:
            item_room_map[i] = room

    for item, room in item_room_map.items():
        if item in bad_items:
            continue
        ic = IntCode(data)
        go_to(ic, start, room, gph)
        out = ic.go_ascii([f"take {item}"])

        if out[-1] == "Command?":
            continue

        for l in reversed(out):
            if not l:
                continue
            symptom = l
            break
        bad_items[item] = symptom

    return bad_items


def collect_items(ic, cur, route, rooms_with_items, gph, bad_items):
    """Collect all the things"""
    take_out = []
    collected_items = set()
    for r in route:
        go_to(ic, cur, r, gph)
        cur = r
        items = rooms_with_items[r]
        for item in items:
            if item in bad_items:
                continue
            out = ic.go_ascii([f"take {item}"])
            take_out.extend(out)
            collected_items.add(item)
    return take_out, cur, collected_items


def try_item_combos(ic, items):
    """Try carrying all the possible combos to get the weight right"""

    def combo_correct(out):
        room = True
        for line in out:
            if "ejected back" in line:
                return False
        return room

    items_idx = list(items)
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

    return out, pwd, items


def manual_explorer(data):
    """Play the game"""

    rooms, gph, rooms_with_items, start, end = auto_explore(data)
    bad_items = get_bad_items(data, gph, start, rooms_with_items)
    print("Don't take these !")
    for k, v in bad_items.items():
        print(f"- {k:20}", v)

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
            out, cur, collected_items = collect_items(
                ic, cur, route, rooms_with_items, gph, bad_items
            )
            continue

        if i == "combos":
            out, pwd, _ = try_item_combos(ic, collected_items)
            out.append(f"Password {pwd}")
            continue

        if i == "solve":
            out, cur, collected_items = collect_items(
                ic, cur, route, rooms_with_items, gph, bad_items
            )
            out, pwd, _ = try_item_combos(ic, collected_items)
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
    bad_items = get_bad_items(data, gph, start, rooms_with_items)
    for k, v in bad_items.items():
        print(f"- {k:20}", v)
    route = plan_route(gph, rooms_with_items, start, end)
    print()
    print(f"Shortest route: {route}")
    ic = IntCode(data)
    _, _, collected_items = collect_items(
        ic, start, route, rooms_with_items, gph, bad_items
    )
    _, pwd, cmb = try_item_combos(ic, collected_items)
    print()
    print(f"Inventory to match weight: {cmb}")
    print()
    visualize_graph(gph)
    return pwd


MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))

# manual_explorer(MY_RAW_DATA)
solve_part_a(MY_RAW_DATA)
