"""Advent of code 2020
--- Day 22: Crab Combat ---
"""

from copy import deepcopy
from common.aoc import file_to_list, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    players = []
    for line in raw_data:
        if line.startswith("Player"):
            deck = []
            continue
        if not line:
            players.append(deck)
            continue
        card = int(line)
        deck.append(card)
    players.append(deck)

    return players


def play_round(decks):
    """Play a round"""
    player_1 = decks[0].pop(0)
    player_2 = decks[1].pop(0)
    if player_1 > player_2:
        decks[0].append(player_1)
        decks[0].append(player_2)
    else:
        decks[1].append(player_2)
        decks[1].append(player_1)


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    decks = deepcopy(data)
    while len(decks[0]) > 0 and len(decks[1]) > 0:
        play_round(decks)
    if len(decks[0]) > 0:
        deck = decks[0]
    else:
        deck = decks[1]
    cards = len(deck)
    ans = sum(card * (cards - idx) for idx, card in enumerate(deck))
    return ans


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""

    def play_game(decks):

        seen_0 = set()
        seen_1 = set()
        while True:

            state = tuple(tuple(deck) for deck in decks)

            if len(decks[0]) == 0 or len(decks[1]) == 0:
                return state

            if state[0] in seen_0 or state[1] in seen_1:
                return (decks[0], [])
            seen_0.add(state[0])
            seen_1.add(state[1])

            card_0 = decks[0].pop(0)
            card_1 = decks[1].pop(0)

            if card_0 > len(decks[0]) or card_1 > len(decks[1]):
                winner = 0
                if card_0 < card_1:
                    winner = 1
            else:
                new_deck_0 = decks[0][:card_0]
                new_deck_1 = decks[1][:card_1]
                new_deck = [new_deck_0, new_deck_1]
                outcome = play_game(new_deck)
                winner = 0
                if len(outcome[0]) == 0:
                    winner = 1

            if winner == 0:
                decks[0].append(card_0)
                decks[0].append(card_1)
            else:
                decks[1].append(card_1)
                decks[1].append(card_0)

    decks = deepcopy(data)
    outcome = play_game(decks)
    deck = outcome[0]
    if len(deck) == 0:
        deck = outcome[1]
    cards = len(deck)
    ans = sum(card * (cards - idx) for idx, card in enumerate(deck))
    return ans


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
