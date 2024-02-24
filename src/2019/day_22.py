"""Advent of code 2019
--- Day 22: Slam Shuffle ---
"""

from itertools import pairwise
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok
from common.numty import mod_exp, mod_inv


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        arr = tok(line)
        if line.startswith("deal with increment"):
            data.append(("inc", int(arr[-1])))
        if line == "deal into new stack":
            data.append(("new", None))
        if line.startswith("cut"):
            data.append(("cut", int(arr[-1])))
    return data


def deal_with_inc(deck, inc):
    """As per spec"""
    sz = len(deck)
    new_deck = [0] * sz
    place_at = 0
    for c in deck:
        new_deck[place_at] = c
        place_at += inc
        place_at %= sz
    return new_deck


def shuffle_a(data, deck):
    """Do the Shuffle"""
    for typ, arg in data:
        if typ == "new":
            deck = list(reversed(deck))
        if typ == "cut":
            deck = deck[arg:] + deck[:arg]
        if typ == "inc":
            deck = deal_with_inc(deck, arg)
    return deck


def previous_position(data, deck_size, cur_pos):
    """Trace the position backwards"""
    for typ, arg in reversed(data):
        if typ == "new":
            cur_pos = deck_size - 1 - cur_pos
        if typ == "cut":
            arg = arg % deck_size
            cur_pos = (cur_pos + arg) % deck_size
        if typ == "inc":
            inv = mod_inv(deck_size, arg)
            cur_pos = (cur_pos * inv) % deck_size
    return cur_pos


@aoc_part
def solve_part_a(data, sz=10) -> int:
    """Solve part A"""
    deck = list(range(sz))
    deck = shuffle_a(data, deck)
    ans = 0
    if sz == 10:
        print(deck)
    else:
        ans = deck.index(2019)

        # test previous_position function for part B
        original_position = previous_position(data, sz, ans)
        assert original_position == 2019

    return ans


def analysis_b(data, deck_size=10007):
    """Some investigation"""

    print()
    print(f"Analysis: Deck size {deck_size}")

    cur_pos = 2020
    previous_positions = [cur_pos]
    while True:
        cur_pos = previous_position(data, deck_size, cur_pos)
        if cur_pos in previous_positions:
            break
        previous_positions.append(cur_pos)

    print(f"Repeats after {len(previous_positions)} shuffles")
    print("1 missing mmm...")

    odd = set(range(deck_size)) - set(previous_positions)
    odd = odd.pop()
    print(f"Missing position {odd}")

    # There must be an operation when repeated which takes every position
    # to every other position except for this odd
    # So it must be a 0 in some kind of multiplication group maybe
    zero = odd
    adjusted = [(p - zero) % deck_size for p in previous_positions]

    assert find_the_zero_element(data, deck_size) == zero

    multipliers = set()
    for a, b in pairwise(adjusted):
        inv_a = mod_inv(deck_size, a)
        m = (b * inv_a) % deck_size
        multipliers.add(m)
    assert len(multipliers) == 1
    m = min(multipliers)
    print(f"Multiplier = {m} after the zero adjustment of {zero}")

    # so we multiply by m as a way of getting to a previous position
    # so the nth previous term will be m^n
    a = adjusted[0]
    for n, p in enumerate(adjusted):
        m_n = mod_exp(m, n, deck_size)
        b = (a * m_n) % deck_size
        assert b == p

    # the multiplier can be found from the first 3 terms
    # b-z = m(a-z)
    # c-z = m(b-z)
    # b-c = m(a-b)
    # m = (a-b)'(b-c)
    a = previous_positions[0]
    b = previous_positions[1]
    c = previous_positions[2]
    inv_a_b = mod_inv(deck_size, a - b)
    m = (inv_a_b * (b - c)) % deck_size
    print(f"Find m = {m} from first 3 terms {a}, {b}, {c} ")

    # now use 2 terms to resolve the zero adjustment
    # m(a-z) = b-z, so
    # z = inv(m-1) x [ma - b]
    a = previous_positions[0]
    b = previous_positions[1]
    inv_m_1 = mod_inv(deck_size, m - 1)
    z = (inv_m_1 * (m * a - b)) % deck_size
    print(f"Find z = {z}")


def find_the_zero_element(data, deck_size):
    """Find the card which always returns to its original place"""
    for p in range(deck_size):
        if p == previous_position(data, deck_size, p):
            return p


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    deck_size = 119315717514047
    shuffles = 101741582076661

    a = 2020
    b = previous_position(data, deck_size, a)
    c = previous_position(data, deck_size, b)

    # find m
    inv_a_b = mod_inv(deck_size, a - b)
    m = (inv_a_b * (b - c)) % deck_size

    # find z
    inv_m_1 = mod_inv(deck_size, m - 1)
    z = (inv_m_1 * (m * a - b)) % deck_size

    # the card in position 2020 will be the top card from
    # 101741582076661 shuffles ago
    # = [(a-z) x m^shuffles] + z
    ans = (a - z) * mod_exp(m, shuffles, deck_size) + z
    ans %= deck_size

    return ans


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA, sz=10007)

analysis_b(MY_DATA)
solve_part_b(MY_DATA)
