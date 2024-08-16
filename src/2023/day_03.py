"""Advent of code 2023
--- Day 3: Gear Ratios ---
"""

from operator import add
from common.aoc import file_to_list, aoc_part, get_filename
from common.grid_2d import all_directions


def parse_data(raw_data):
    """Parse the input"""
    return raw_data


def get_symbol_locations(data):
    """Return a dict of symbol locations"""
    symbols = {}
    for ri, row in enumerate(data):
        for ci, content in enumerate(row):
            if content.isdigit() or content == ".":
                continue
            p = (ri, ci)
            symbols[p] = content
    return symbols


def get_part_numbers(data: list) -> list:
    """Return a list of part numbers with their location in the grid"""
    part_numbers = []
    for r, row in enumerate(data):
        pn = ""
        from_col = None
        for c, ch in enumerate(row):
            if ch.isdigit():
                pn += ch
                if from_col is None:
                    from_col = c
            else:
                # store the part number along with the row, col & length
                if pn:
                    part_number = (int(pn), r, from_col, len(pn))
                    part_numbers.append(part_number)
                    pn = ""
                    from_col = None
        if pn:
            part_number = (int(pn), r, from_col, len(pn))
            part_numbers.append(part_number)
    return part_numbers


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    symbols = get_symbol_locations(data)
    potential_part_numbers = get_part_numbers(data)
    part_numbers = []
    for pn, r, c, l in potential_part_numbers:

        # check all places adjacent to every digit for
        # a symbol of some kind
        is_a_part_number = False
        for x in range(c, c + l):
            pos = (r, x)
            for d in all_directions:
                n = tuple(map(add, pos, d))
                if n in symbols:
                    part_numbers.append(pn)
                    is_a_part_number = True
                    break
            if is_a_part_number:
                break

    return sum(part_numbers)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    symbols = get_symbol_locations(data)
    potential_part_numbers = get_part_numbers(data)

    # build a dictionary of locations and the index of the part number
    # that exist there
    location_values = {}
    for i, (_, r, c, l) in enumerate(potential_part_numbers):
        for x in range(c, c + l):
            location_values[(r, x)] = i

    total = 0
    for pos, sym in symbols.items():
        if sym != "*":
            continue

        # find all the part numbers adjacent to the *
        values = set()
        for d in all_directions:
            n = tuple(map(add, pos, d))
            if n in location_values:
                values.add(location_values[n])

        # if there are exactly 2 get their product
        gear_prod = 0
        if len(values) == 2:
            a = values.pop()
            b = values.pop()
            gear_prod = potential_part_numbers[a][0] * potential_part_numbers[b][0]
        total += gear_prod

    return total


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
