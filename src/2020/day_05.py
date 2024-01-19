"""Advent of code 2020
--- Day 5: Binary Boarding ---
"""

from common.aoc import file_to_list, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    data = raw_data
    data = []
    for p in raw_data:
        p: str
        p = p.replace("B", "1")
        p = p.replace("R", "1")
        p = p.replace("F", "0")
        p = p.replace("L", "0")
        d = int(p, 2)
        data.append(d)
    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    return max(data)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    max_row = max(data) // 8
    min_row = (min(data) // 8) + 1
    valid_seats = {s for s in range(min_row * 8, max_row * 8 + 1)}
    listed = set(data)
    valid_seats.difference_update(listed)
    return valid_seats.pop()


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

# solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
