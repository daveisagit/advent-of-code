"""Advent of code 2015
--- Day 21: RPG Simulator 20XX ---
"""

from itertools import combinations, product
from math import inf
from operator import add
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok

WEAPONS = {
    "Dagger": (8, 4, 0),
    "Shortsword": (10, 5, 0),
    "Warhammer": (25, 6, 0),
    "Longsword": (40, 7, 0),
    "Greataxe": (74, 8, 0),
}

ARMOUR = {
    "(none)": (0, 0, 0),
    "Leather": (13, 0, 1),
    "Chainmail": (31, 0, 2),
    "Splintmail": (53, 0, 3),
    "Bandedmail": (75, 0, 4),
    "Platemail": (102, 0, 5),
}

RINGS = {
    "(none)1": (0, 0, 0),
    "(none)2": (0, 0, 0),
    "Damage +1": (25, 1, 0),
    "Damage +2": (50, 2, 0),
    "Damage +3": (100, 3, 0),
    "Defense +1": (20, 0, 1),
    "Defense +2": (40, 0, 2),
    "Defense +3": (80, 0, 3),
}


def parse_data(raw_data):
    """Parse the input"""
    boss = []
    for line in raw_data:
        arr = tok(line, ":")
        boss.append(int(arr[1]))
    return tuple(boss)


def options(gold):
    """Generate gear options"""
    for w, a, r in product(
        WEAPONS.values(), ARMOUR.values(), combinations(RINGS.values(), 2)
    ):
        combo = tuple(map(add, w, a))
        combo = tuple(map(add, combo, r[0]))
        combo = tuple(map(add, combo, r[1]))
        if combo[0] <= gold:
            yield combo[0], combo[1], combo[2]


def player_wins(player, boss):
    """Return True if so"""
    player = list(player)
    boss = list(boss)
    while True:
        damage = max(player[1] - boss[2], 1)
        boss[0] -= damage
        if boss[0] <= 0:
            return True
        damage = max(boss[1] - player[2], 1)
        player[0] -= damage
        if player[0] <= 0:
            return False


@aoc_part
def solve_part_a(boss) -> int:
    """Solve part A"""
    gold = 0
    while True:
        for _, damage, amour in options(gold):
            player = (100, damage, amour)
            if player_wins(player, boss):
                return gold
        gold += 1


@aoc_part
def solve_part_b(boss) -> int:
    """Solve part B"""

    gold = inf
    spend = []
    for cost, damage, amour in options(gold):
        player = (100, damage, amour)
        if not player_wins(player, boss):
            spend.append(cost)
    return max(spend)


MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(MY_DATA)

solve_part_b(MY_DATA)
