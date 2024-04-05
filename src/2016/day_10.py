"""Advent of code 2016
--- Day 10: Balance Bots ---
"""

from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass, field
import re
from common.aoc import file_to_list, aoc_part, get_filename


@dataclass
class Bot:
    """You bot yer"""

    my_id: int
    low_type: str
    low_id: int
    high_type: str
    high_id: int
    has: list = field(default_factory=list)

    def count(self):
        """How many!"""
        return len(self.has)

    def has_2(self):
        """Ready to give"""
        if len(self.has) > 1:
            return True
        return False

    @property
    def low_val(self):
        """Low value"""
        return min(self.has)

    @property
    def high_val(self):
        """High value"""
        return max(self.has)


def parse_data(raw_data):
    """Parse the input"""
    bots = {}
    for line in raw_data:
        if line[:3] == "bot":
            rr = re.search(
                r"bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)",
                line,
            )
            bot = Bot(
                int(rr.group(1)),
                rr.group(2),
                int(rr.group(3)),
                rr.group(4),
                int(rr.group(5)),
            )
            bots[int(rr.group(1))] = bot

    for line in raw_data:
        if line[:5] == "value":
            rr = re.search(
                r"value (\d+) goes to bot (\d+)",
                line,
            )
            bots[int(rr.group(2))].has.append(int(rr.group(1)))

    return bots


def go_bots(bots, target=None):
    """Run the bots"""
    outputs = defaultdict(int)
    ans = None
    while True:
        bots_ready = [b for b in bots.values() if b.has_2()]
        if not bots_ready:
            break
        for bot in bots_ready:
            bot: Bot

            if set(bot.has) == target:
                ans = bot.my_id

            if bot.low_type == "output":
                outputs[bot.low_id] = bot.low_val
            else:
                bots[bot.low_id].has.append(bot.low_val)
            bot.has.remove(bot.low_val)

            if bot.high_type == "output":
                outputs[bot.high_id] = bot.high_val
            else:
                bots[bot.high_id].has.append(bot.high_val)
            bot.has.remove(bot.high_val)

    return ans, outputs


@aoc_part
def solve_part_a(bots, target=None) -> int:
    """Solve part A"""
    ans, _ = go_bots(bots, target)
    return ans


@aoc_part
def solve_part_b(bots) -> int:
    """Solve part B"""
    _, outputs = go_bots(bots)
    ans = outputs[0] * outputs[1] * outputs[2]
    return ans


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(deepcopy(EX_DATA), target={2, 5})
solve_part_a(deepcopy(MY_DATA), target={17, 61})

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
