"""Advent of code 2021
--- Day 4: Giant Squid ---
"""

from common.aoc import file_to_list, aoc_part, get_filename
from common.general import get_column, tok, window_over


def parse_data(raw_data):
    """Parse the input"""
    balls = tok(raw_data[0], delim=",")
    balls = [int(n) for n in balls]
    cards = []
    for w in window_over(raw_data[2:], 5, 6):
        card = []
        for l in w:
            card.append([int(n) for n in tok(l) if n])
        cards.append(card)
    return balls, cards


def make_lines(cards: list) -> list:
    """Create an array of lines 10 per card"""
    lines = []
    for card in cards:
        for idx in range(5):
            lines.append(set(get_column(card, idx)))
            lines.append(set(card[idx]))
    return lines


def play_bingo_to_first_winner(balls: list, lines: list) -> tuple:
    """Return the winning ball index and card #"""
    for ball_idx, ball in enumerate(balls):
        for line_index, line in enumerate(lines):
            if ball not in line:
                continue
            line.remove(ball)
            if not line:
                card_index = line_index // 10
                return ball_idx, card_index
    return None


def play_bingo_to_the_death(balls: list, lines: list) -> tuple:
    """Return the very last ball index and card #"""
    cards_complete = set()
    for ball_idx, ball in enumerate(balls):
        for line_index, line in enumerate(lines):
            if ball not in line:
                continue

            line.remove(ball)
            if line:
                continue

            card_index = line_index // 10
            cards_complete.add(card_index)
            if len(cards_complete) == len(lines) // 10:
                return ball_idx, card_index
    return None


def solve(balls, cards, play_func) -> int:
    """Solve generally for a given play bingo function"""
    lines = make_lines(cards)
    winning_ball_index, winning_card = play_func(balls, lines)

    card_content = set()
    for lines in cards[winning_card]:
        card_content.update(lines)

    for ball in balls[: winning_ball_index + 1]:
        if ball in card_content:
            card_content.remove(ball)

    return sum(card_content) * balls[winning_ball_index]


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    balls = data[0]
    cards = data[1]
    return solve(balls, cards, play_bingo_to_first_winner)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    balls = data[0]
    cards = data[1]
    return solve(balls, cards, play_bingo_to_the_death)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
