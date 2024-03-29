"""Advent of code 2018
--- Day 24: Immune System Simulator 20XX ---
"""

from dataclasses import dataclass
import re
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


@dataclass
class Group:
    """As per the puzzle"""

    army: str
    index: int
    regiment: int
    units: int
    hit_points: int
    attack_damage: int
    attack_type: str
    initiative: int
    weaknesses: list
    immunities: list

    def __post_init__(self):
        self.initial_units = self.units
        self.boost = 0

    def __str__(self) -> str:
        return f"""Army: {self.army}       Regiment: {self.regiment}    Units: {self.units}
        Hit Points:      {self.hit_points}
        Attack Damage:   {self.attack_damage} 
        Attack Type:     {self.attack_type} 
        Initiative:      {self.initiative}
        Weaknesses:      {str(self.weaknesses)} 
        Immunities:      {str(self.immunities)}
        Effective Power: {self.effective_power}"""

    @property
    def effective_power(self) -> int:
        """units x attack damage"""
        return self.units * (self.attack_damage + self.boost)

    def reset(self, boost=0):
        """Reset the group with a boost"""
        self.units = self.initial_units
        if self.army == "Immune System":
            self.boost = boost


def parse_data(raw_data):
    """Parse the input"""
    army_name = None
    groups = []
    index = 0
    regiment = 0
    for line in raw_data:
        if not army_name:
            army_name = line[:-1]
            regiment = 0
            continue
        if not line:
            army_name = None
            continue

        if "(" in line:
            result = re.search(
                r"(\d+) units each with (\d+) hit points \((.+)\) with an attack that does (\d+) (.+) damage at initiative (\d+)",
                line,
            )
        else:
            result = re.search(
                r"(\d+) units each with (\d+) hit points(.*)with an attack that does (\d+) (.+) damage at initiative (\d+)",
                line,
            )

        weaknesses = []
        immunities = []
        extras = result.group(3)
        for extra in tok(extras, ";"):
            if not extra:
                continue
            arr = tok(extra, " to ")
            things = list(tok(arr[1], ","))
            if arr[0] == "weak":
                weaknesses = things
            if arr[0] == "immune":
                immunities = things

        regiment += 1
        g = Group(
            army_name,
            index,
            regiment,
            int(result.group(1)),
            int(result.group(2)),
            int(result.group(4)),
            result.group(5),
            int(result.group(6)),
            tuple(weaknesses),
            tuple(immunities),
        )
        index += 1
        groups.append(g)

    return groups


def target_selection(groups, dump=False):
    """Return each group's target options"""

    def get_attacking_options(attacker):
        options = []
        for defender in groups:
            # same side
            if defender.army == attacker.army:
                continue
            # out the game
            if defender.units <= 0:
                continue

            damage = attacker.attack_damage + attacker.boost
            if attacker.attack_type in defender.immunities:
                damage = 0
            if attacker.attack_type in defender.weaknesses:
                damage *= 2
            if damage > 0:
                options.append((defender, damage))

        options = sorted(
            options,
            key=lambda x: (x[1], x[0].effective_power, x[0].initiative),
            reverse=True,
        )
        return options

    # who's alive and who's next
    active_groups = [g for g in groups if g.units > 0]
    turn_order = sorted(
        active_groups, key=lambda x: (x.effective_power, x.initiative), reverse=True
    )

    # fights is a list of (attacker, defender, damage/unit)
    fights = []
    defenders = set()
    for attacker in turn_order:
        attacking_options = get_attacking_options(attacker)

        for o in attacking_options:
            d_idx = o[0].index
            if dump:
                print(
                    f"{attacker.army:15} {attacker.regiment:4} {groups[d_idx].regiment:4} {o[1]*attacker.units:7}"
                )
            if d_idx not in defenders:
                defenders.add(d_idx)
                fights.append((attacker.index, d_idx, o[1]))
                break

    # ordered by attackers initiative
    fights = sorted(fights, key=lambda x: groups[x[0]].initiative, reverse=True)

    return fights


def attacking_phase(groups, fights):
    """Resolve the fights, applying damage to defenders"""
    for a, d, damage in fights:
        attacker = groups[a]
        defender = groups[d]
        if attacker.units == 0:
            continue
        damage *= attacker.units
        kills = damage // defender.hit_points
        kills = min(kills, defender.units)
        defender.units -= kills


def resolve_battle(groups, boost=0):
    """Who won and by what"""
    for g in groups:
        g.reset(boost=boost)

    prv_unit_sum = -1
    while True:
        active_groups = [g for g in groups if g.units > 0]
        unit_sum = sum(g.units for g in active_groups)
        if unit_sum == prv_unit_sum:
            return "Draw", 0
        prv_unit_sum = unit_sum
        armies = {g.army for g in active_groups}
        if len(armies) < 2:
            break
        fights = target_selection(groups, dump=False)
        attacking_phase(groups, fights)

    active_groups = [g for g in groups if g.units > 0]
    units = sum(g.units for g in active_groups)
    return active_groups[0].army, units


@aoc_part
def solve_part_a(groups) -> int:
    """Solve part A"""
    _, units = resolve_battle(groups)
    return units


def search_for_immune_win(groups):
    """Binary search"""
    d = 1
    boost = 0
    target_reached = False
    while True:

        if target_reached:
            if abs(d) > 1:
                d //= 2
            boost += d
        else:
            d *= 2
            boost = d

        winner, units = resolve_battle(groups, boost=boost)

        if winner == "Immune System" and d > 0:
            if d == 1:
                break
            if not target_reached:
                target_reached = True
            d = -d
            continue

        if winner != "Immune System" and d < 0:
            d = -d

    return units, boost


@aoc_part
def solve_part_b(groups) -> int:
    """Solve part B"""
    units, _ = search_for_immune_win(groups)
    return units


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
