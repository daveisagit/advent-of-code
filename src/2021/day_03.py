"""Advent of code 2021
--- Day 3: Binary Diagnostic ---
"""

from collections import Counter
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import get_column


def parse_data(raw_data):
    """Parse the input"""
    data = raw_data
    return data


def get_gamma(data):
    """Get the gamma value for the data"""
    gamma = []
    word_length = len(data[0])
    for col in range(word_length):
        column = get_column(data, col)
        bit_count = Counter(column)
        tally = bit_count.most_common()
        bit = tally[0][0]
        gamma.append(bit)
    gamma = "".join(gamma)
    gamma = int(gamma, 2)
    return gamma


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    gamma = get_gamma(data)
    word_length = len(data[0])
    epsilon = 2**word_length - 1 - gamma
    return gamma * epsilon


def get_bit_for_column_ogr(data, col):
    """For a given set of values return the bit value for the most common
    in the column or 1 if equal"""
    column = get_column(data, col)
    bit_count = Counter(column)
    tally = bit_count.most_common()
    bit = tally[0][0]  # most common (1st)
    if tally[0][1] == tally[1][1]:
        bit = "1"
    return bit


def get_bit_for_column_csr(data, col):
    """For a given set of values return the bit value for the least common
    in the column or 0 if equal"""
    column = get_column(data, col)
    bit_count = Counter(column)
    tally = bit_count.most_common()
    bit = tally[1][0]  # least common (2nd)
    if tally[0][1] == tally[1][1]:
        bit = "0"
    return bit


def get_single_value(data, get_bit_func):
    """Get the OGR value for the data"""
    word_length = len(data[0])
    current_data = data.copy()
    for col in range(word_length):
        bit = get_bit_func(current_data, col)
        current_data = [b for b in current_data if b[col] == bit]
        if len(current_data) == 1:
            return current_data[0]


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    ogr = get_single_value(data, get_bit_for_column_ogr)
    csr = get_single_value(data, get_bit_for_column_csr)
    ogr = int(ogr, 2)
    csr = int(csr, 2)
    return ogr * csr


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
