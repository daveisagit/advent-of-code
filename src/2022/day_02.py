"""Advent of code 2022
--- Day 2: Rock Paper Scissors ---

0: Rock
1: Paper
2: Scissors

        Us
elf |  0   1   2
----------------
0   |  3   6   0
1   |  0   3   6
2   |  6   0   3


        Us
elf |  0   1   2 |   adj
-----------------------
0   |  1   2   0 |   1
1   |  0   1   2 |   2
2   |  2   0   1 |   0    

result score =  elf + us + adj (mod 3)

"""

from common.aoc import file_to_list, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    elf = "ABC"
    our = "XYZ"
    rounds = [(elf.index(line[0]), our.index(line[2])) for line in raw_data]
    return rounds


def score(elf, us) -> int:
    adj = (1, 2, 0)
    score = adj[elf] + elf + us
    score %= 3
    score *= 3
    score += us + 1
    return score


def hand_choice(elf, outcome) -> int:
    """
          Adj
    Win   +1
    Draw   0
    lose  -1
    """
    return (elf + outcome - 1) % 3


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    return sum(score(elf, us) for elf, us in data)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    return sum(score(elf, hand_choice(elf, us)) for elf, us in data)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
