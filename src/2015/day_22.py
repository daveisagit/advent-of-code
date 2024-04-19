"""Advent of code 2015
--- Day 22: Wizard Simulator 20XX ---
"""

from heapq import heappop, heappush
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    boss = []
    for line in raw_data:
        arr = tok(line, ":")
        boss.append(int(arr[1]))
    return tuple(boss)


def least_mana(boss, player, part_b=False):
    """Mana budget"""
    state = (0, "player", boss, player, 0, 0, 0)
    h = []
    heappush(h, state)
    while h:
        state = heappop(h)
        mana_spent, turn, boss, player, poison, recharge, shield = state

        if part_b:
            if turn == "player":
                player = (player[0] - 1, player[1])

        if player[0] <= 0:
            continue

        # Effects
        player_armour = 0
        if shield:
            player_armour = 7
            shield -= 1
        if poison:
            boss = (boss[0] - 3, boss[1])
            poison -= 1
        if recharge:
            player = (player[0], player[1] + 101)
            recharge -= 1

        # We won!
        if boss[0] <= 0:
            return mana_spent

        # Take the beating
        if turn == "boss":
            damage = max(boss[1] - player_armour, 1)
            new_player = (player[0] - damage, player[1])
            state = mana_spent, "player", boss, new_player, poison, recharge, shield
            heappush(h, state)

        if turn == "player":

            # Magic missile
            if player[1] >= 53:
                new_boss = (boss[0] - 4, boss[1])
                new_player = (player[0], player[1] - 53)
                state = (
                    mana_spent + 53,
                    "boss",
                    new_boss,
                    new_player,
                    poison,
                    recharge,
                    shield,
                )
                heappush(h, state)

            # Drain
            if player[1] >= 73:
                new_boss = (boss[0] - 2, boss[1])
                new_player = (player[0] + 2, player[1] - 73)
                state = (
                    mana_spent + 73,
                    "boss",
                    new_boss,
                    new_player,
                    poison,
                    recharge,
                    shield,
                )
                heappush(h, state)

            # Shield
            if player[1] >= 113 and shield == 0:
                new_player = (player[0], player[1] - 113)
                state = (
                    mana_spent + 113,
                    "boss",
                    boss,
                    new_player,
                    poison,
                    recharge,
                    6,
                )
                heappush(h, state)

            # Poison
            if player[1] >= 173 and poison == 0:
                new_player = (player[0], player[1] - 173)
                state = (
                    mana_spent + 173,
                    "boss",
                    boss,
                    new_player,
                    6,
                    recharge,
                    shield,
                )
                heappush(h, state)

            # Recharge
            if player[1] >= 229 and recharge == 0:
                new_player = (player[0], player[1] - 229)
                state = (
                    mana_spent + 229,
                    "boss",
                    boss,
                    new_player,
                    poison,
                    5,
                    shield,
                )
                heappush(h, state)


@aoc_part
def solve_part_a(boss, player=(10, 250)) -> int:
    """Solve part A"""
    return least_mana(boss, player)


@aoc_part
def solve_part_b(boss, player=(50, 500)) -> int:
    """Solve part B"""
    return least_mana(boss, player, part_b=True)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

# solve_part_a(EX_DATA)
# solve_part_a(MY_DATA, player=(50, 500))

# solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
