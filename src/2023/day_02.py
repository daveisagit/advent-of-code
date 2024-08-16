"""Advent of code 2023
--- Day 2: Cube Conundrum ---
"""

from collections import defaultdict
from math import prod
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok

COLOUR_LIMITS = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def parse_data(raw_data):
    """Return the data structure for the raw input.
    A list of games
    A game is a list of hands
    A hand is a dict of cube counts
    """
    games = []
    for line in raw_data:
        # we only need the right part as the game # is just an index
        arr = tok(line, delim=":")

        # handfuls are split by semi-colon ;
        raw_hands = tok(arr[1], delim=";")
        hands = []
        for raw_hand in raw_hands:
            # cube data is split by comma ,
            raw_cubes = tok(raw_hand, delim=",")
            hand = {}
            for raw_cube_count in raw_cubes:
                cube_data = tok(raw_cube_count)
                hand[cube_data[1]] = int(cube_data[0])

            hands.append(hand)

        games.append(hands)

    return games


def is_a_possible_game(game: list) -> bool:
    """Return True if its possible"""
    for hand in game:
        for colour, limit in COLOUR_LIMITS.items():
            if hand.get(colour, 0) > limit:
                return False
    return True


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    return sum(idx + 1 for idx, game in enumerate(data) if is_a_possible_game(game))


def get_minimum_values(game: list) -> dict:
    """Find the minimum values for a game"""
    colours = COLOUR_LIMITS.keys()
    minimum_values = defaultdict(int)
    for colour in colours:
        minimum_values[colour] = max([hand.get(colour, 0) for hand in game], default=0)
    return minimum_values


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    return sum(prod(get_minimum_values(game).values()) for game in data)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
