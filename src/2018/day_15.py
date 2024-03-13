"""Advent of code 2018
--- Day 15: Beverage Bandits ---
"""

from collections import defaultdict
from copy import deepcopy
from operator import add
from common.aoc import file_to_list, aoc_part, get_filename
from common.graph import dijkstra
from common.grid_2d import directions


def parse_data(raw_data):
    """Parse the input"""
    units = []
    nodes = set()
    gph = defaultdict(dict)
    for r, line in enumerate(raw_data):
        for c, ch in enumerate(line):
            p = (r, c)
            if ch == "#":
                continue
            nodes.add(p)
            if ch == ".":
                continue
            unit = [ch, p, 200]
            units.append(unit)

    for p in nodes:
        for d in directions.values():
            n = tuple(map(add, p, d))
            if n in nodes:
                gph[p][n] = 1

    map_height = len(raw_data)
    map_width = len(raw_data[0])

    return gph, units, map_height, map_width


def movement_graph(gph, units, unit_id):
    """Create a graph that excludes spots where there are other units"""
    g = deepcopy(gph)
    for iu, unit in enumerate(units):
        hp = unit[2]
        # ignore this unit as well as eliminated ones
        if iu == unit_id or hp <= 0:
            continue
        # remove neighbours and the node
        u = unit[1]
        for v in g[u]:
            del g[v][u]
        del g[u]
    return g


def get_targets(gph, units, unit_id):
    """Return a set of target locations: unoccupied neighbouring tiles of the enemy"""
    other_unit_locations = {
        u[1] for i, u in enumerate(units) if i != unit_id and u[2] > 0
    }
    target_type = "G"
    if units[unit_id][0] == target_type:
        target_type = "E"

    targets = set()
    target_units = [u for u in units if u[0] == target_type and u[2] > 0]
    for target_unit in target_units:
        u = target_unit[1]
        for v in gph[u]:
            if v in other_unit_locations:
                continue
            targets.add(v)

    return targets


def move_unit(gph, units, unit_id):
    """Pick your target, and move towards it"""
    u = units[unit_id][1]
    targets = get_targets(gph, units, unit_id)
    if not targets:
        return

    if u in targets:
        # already there
        return

    mg = movement_graph(gph, units, unit_id)
    dd = dijkstra(mg, u, None)
    dd = {p: d for p, d in dd.items() if p in targets}
    if not dd:
        # no reachable target
        return

    closest = min(dd.values())
    closest_targets = {p for p, d in dd.items() if d == closest}
    closest_target = sorted(closest_targets)[0]

    dd_back = dijkstra(mg, closest_target, None)
    dd_back = {p: d for p, d in dd_back.items() if p in mg[u]}
    closest = min(dd_back.values())
    closest_next_tiles = {v for v in mg[u] if dd_back[v] == closest}
    closest_next_tile = sorted(closest_next_tiles)[0]
    units[unit_id][1] = closest_next_tile


def draw_map(gph, units, map_height, map_width):
    """Visual"""
    team = {u[1]: u for u in units}
    for r in range(map_height):
        row = ""
        hps = ""
        for c in range(map_width):
            p = (r, c)
            ch = "#"
            if p in gph:
                ch = "."
            if p in team and team[p][2] > 0:
                ch = team[p][0]
                hps = f"{hps} {ch}({team[p][2]})"
            row += ch
        row += hps

        print(row)
    print()


def unit_attacks(gph, units, unit_id, elf_power=3):
    """Attack!!"""
    unit = units[unit_id]
    p = unit[1]
    active_enemy_units_adjacent = [
        i
        for i, u in enumerate(units)
        if u[2] > 0 and u[0] != unit[0] and u[1] in gph[p]
    ]

    if not active_enemy_units_adjacent:
        return

    lowest_hit_point = min(units[i][2] for i in active_enemy_units_adjacent)
    weakest = [
        i for i in active_enemy_units_adjacent if units[i][2] == lowest_hit_point
    ]
    victim = sorted(weakest, key=lambda k: units[k][1])[0]
    damage = 3
    if units[victim][0] == "G":
        damage = elf_power
    units[victim][2] -= damage


def get_turn_order(units):
    """Return a list of indexes"""
    turn_order = sorted(range(len(units)), key=lambda k: units[k][1])
    turn_order = [i for i in turn_order if units[i][2] > 0]
    return turn_order


def do_round(gph, units, elf_power=3):
    """Move and attack, return False if the game is over before
    all units have had their turn"""
    turn_order = get_turn_order(units)
    for idx in turn_order:
        active_teams = {u[0] for u in units if u[2] > 0}
        if len(active_teams) == 1:
            # we have a winning team
            return False
        if units[idx][2] <= 0:
            # if this unit is now dead do not move or attack
            continue
        move_unit(gph, units, idx)
        unit_attacks(gph, units, idx, elf_power=elf_power)
    return True


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    data = deepcopy(data)
    gph, units, map_height, map_width = data
    # print("Start")
    # draw_map(gph, units, map_height, map_width)

    r = 0
    while True:
        if not do_round(gph, units):
            break
        r += 1
        # print(f"After round {r}")
        # draw_map(gph, units, map_height, map_width)

    # print("Finish")
    # draw_map(gph, units, map_height, map_width)

    remaining_units_hit_point_sum = sum(u[2] for u in units if u[2] > 0)

    return remaining_units_hit_point_sum * r


def try_elf_power(data, elf_power):
    """Try it out"""
    gph, units, map_height, map_width = data
    r = 0
    while True:
        if not do_round(gph, units, elf_power=elf_power):
            break
        r += 1
        # print(f"After round {r}")
        # draw_map(gph, units, map_height, map_width)
    return r


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    _, units, _, _ = data
    elf_units = len([u for u in units if u[0] == "E"])
    ep = 3
    adj = 8
    while True:
        ep += adj
        d = deepcopy(data)
        _, units, _, _ = d
        rounds = try_elf_power(d, ep)
        active_elf_units = len([u for u in units if u[0] == "E" and u[2] > 0])

        if active_elf_units == elf_units:
            if adj == 1:
                break
            if adj > 0:
                adj = -adj // 2
                continue
        else:
            if adj < 0:
                adj = -adj

    remaining_units_hit_point_sum = sum(u[2] for u in units if u[0] == "E")

    return remaining_units_hit_point_sum * rounds


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)


MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)


solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
