"""Advent of code 2021
--- Day 21: Dirac Dice ---
Strange that for part B, the example took longer than my data
Can't just ignore a repeat find of a given state since it still
contributes to the number of universes.

Probably a more efficient method a simple seen set gives
acceptable runtime, but invalidates the result.

So maybe a weighted graph of states, where the weight is the
number of universes for that roll. Then for each final state
calc the product of the weights on every path from initial and
sum these product paths for a value for the final state.
"""

from collections import defaultdict, deque, namedtuple
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        arr = tok(line, delim=":")
        data.append(int(arr[1]))
    return data


def moved(player, n):
    """the number of tiles moved by a player"""
    if player == 0:
        return 9 * n * (n + 1) - 12 * n
    return 9 * n * (n + 1) - 3 * n


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    scores = [0] * 2
    n = 0
    while True:
        n += 1
        for player, start in enumerate(data):
            p = (moved(player, n) + start) % 10
            score = scores[player] + (10 if p == 0 else p)
            scores[player] = score
            if score >= 1000:
                rolls = (n * 2 + player - 1) * 3
                losing_score = scores[(player + 1) % 2]
                return rolls * losing_score


State = namedtuple(
    "State",
    ["last_player", "scores", "positions", "universes"],
)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""

    def make_options():
        """A dict of the outcomes and the universe count"""
        options = defaultdict(int)
        for a in range(1, 4):
            for b in range(1, 4):
                for c in range(1, 4):
                    t = a + b + c
                    options[t] += 1
        return options

    options = make_options()

    game = deque()  # BFS of the outcomes
    # player 0 vs player 1, so initially player 1 was last to play
    initial = State(1, (0, 0), tuple(data), 1)
    game.append(initial)
    wins = [0] * 2
    # seen = set()
    while game:
        state: State = game.pop()
        # if state in seen:
        #     continue
        # seen.add(state)

        if max(state.scores) >= 21:
            wins[state.last_player] += state.universes
            continue

        next_player = (state.last_player + 1) % 2
        for mv, uni_cnt in options.items():
            scores = list(state.scores)
            positions = list(state.positions)

            next_position = positions[next_player] + mv
            next_position = next_position % 10
            score_inc = 10 if next_position == 0 else next_position

            positions[next_player] = next_position
            scores[next_player] += score_inc
            universes = state.universes * uni_cnt

            new_state = State(next_player, tuple(scores), tuple(positions), universes)
            game.append(new_state)

    print(wins)
    return max(wins)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
