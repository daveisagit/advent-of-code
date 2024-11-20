"""Advent of code 2019
--- Day 14: Space Stoichiometry ---
"""

from collections import defaultdict
from math import ceil
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import binary_search, tok


def parse_data(raw_data):
    """Parse the input, create 2 DAGs where the edge is (a,b)
    FUEL -> ORE : requires (a=batch size, b=amount required)
    ORE -> FUEL : contributes ( a,b swapped)
    """

    def amt(s):
        a = tok(s)
        return int(a[0]), a[1]

    contributes = defaultdict(dict)
    requires = defaultdict(dict)
    for line in raw_data:
        arr = tok(line, "=>")
        makes = amt(arr[1])[0]
        item = amt(arr[1])[1]
        lst = tok(arr[0], ",")
        lst = [(amt(x)[0], amt(x)[1]) for x in lst]

        for qty, ingredient in lst:
            requires[item][ingredient] = (makes, qty)
            contributes[ingredient][item] = (qty, makes)

    return requires, contributes


def ore_required(data, fuel=1):
    """Return the ore required"""
    _, contributes = data

    def amount_required(ingredient):
        if ingredient not in contributes:
            return fuel
        total = 0
        for item, (required, batch_size) in contributes[ingredient].items():
            r = amount_required(item)
            batches = int(ceil(r / batch_size))
            made = required * batches
            total += made

        return total

    return amount_required("ORE")


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    return ore_required(data)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    one_fuel = ore_required(data)
    trillion = 10**12

    # rough estimate
    est_fuel = trillion // one_fuel
    ore = ore_required(data, fuel=est_fuel)

    # refined estimate (now we have a ratio closer to reality)
    est_fuel = est_fuel * trillion // ore
    ore = ore_required(data, fuel=est_fuel)

    # zoom in on the exact value
    inc = 1
    if ore > trillion:
        inc = -1

    fuel_a = est_fuel
    ore_a = ore
    while True:
        fuel_b = fuel_a + inc
        ore_b = ore_required(data, fuel=fuel_b)
        if inc == 1 and ore_a <= trillion < ore_b:
            return fuel_a
        if inc == -1 and ore_b <= trillion < ore_a:
            return fuel_b
        fuel_a = fuel_b
        ore_a = ore_b


@aoc_part
def solve_part_c(data) -> int:
    trillion = 10**12

    def f(x):
        return ore_required(data, fuel=x)

    ore = binary_search(f, target=trillion, bound="upper")
    return ore


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)

solve_part_c(MY_DATA)
