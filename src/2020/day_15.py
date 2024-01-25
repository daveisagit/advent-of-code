"""Advent of code 2020
--- Day 15: Rambunctious Recitation ---
"""

from collections import defaultdict
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    data = [int(x) for x in tok(raw_data[0], ",")]
    return data


def play(data: list, rounds=2020):
    """Play the game"""
    state: list = data.copy()
    state = list(reversed(state))
    for _ in range(rounds - len(state)):
        lst_n = state[0]
        try:
            lst_p = state[1:].index(lst_n) + 1
        except ValueError:
            lst_p = 0
        state.insert(0, lst_p)
    return state


def play_b_q(data: list, rounds=2020):
    """Play the game, faster than part A
    Do keeping looking into the past, just remember
    the relevant bits, using a mini queue of 2 for each
    spoken number."""

    # remember the last time a number was spoken
    spoken_at = defaultdict(list)
    for p, x in enumerate(data):
        spoken_at[x].append(p)

    this_number = data[-1]

    for r in range(len(data), rounds):
        # by default the next number is zero unless
        # we know the last time
        next_number = 0
        if len(spoken_at[this_number]) == 2:
            next_number = spoken_at[this_number][1] - spoken_at[this_number][0]

        # remember this occurrence
        spoken_at[next_number].append(r)
        if len(spoken_at[next_number]) > 2:
            spoken_at[next_number].pop(0)

        this_number = next_number

    return this_number


def play_b(data: list, rounds=2020):
    """Play the game: A refinement on the above since the mini queue
    is an over head not really needed, from 20s down to 8s."""

    # remember the last time a number was spoken
    # initialised for all except the last bit of input
    spoken_at = {}
    for p, x in enumerate(data[:-1]):
        spoken_at[x] = p

    # start with the last bit of input
    this_number = data[-1]

    # the first n rounds are given by the input
    for r in range(len(data), rounds):
        # we are checking and setting using the previous
        # round
        prev_round = r - 1

        # by default the next number is zero unless
        # there was a previous mention
        next_number = 0
        if this_number in spoken_at:
            next_number = prev_round - spoken_at[this_number]

        # now that we've used spoken_at[this_number] we can
        # update it
        spoken_at[this_number] = prev_round

        this_number = next_number

    return this_number


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    state = play(data)
    return state[0]


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    return play_b(data, rounds=30000000)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
