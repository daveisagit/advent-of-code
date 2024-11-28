"""Advent of code 2020
--- Day 21: Allergen Assessment ---
"""

from collections import defaultdict
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok
from common.logic import mapping_options, resolve_injective_mappings


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        arr = tok(line, "(contains")
        ingredients = set(tok(arr[0]))
        allergens = set(tok(arr[1][:-1], ","))
        data.append((ingredients, allergens))
    return data


def get_product_sets(data):
    """Return 2 dictionaries allergens, ingredients with the product indexes
    in which they are contained"""
    ingredient_products = defaultdict(set)
    allergen_products = defaultdict(set)
    for product_num, (ingredients, allergens) in enumerate(data):
        for allergen in allergens:
            allergen_products[allergen].add(product_num)
        for ingredient in ingredients:
            ingredient_products[ingredient].add(product_num)
    return allergen_products, ingredient_products


def get_possibilities(data):
    """Return a dictionary keyed on allergen with a set of the possible ingredients"""
    possible = defaultdict(set)
    allergen_products, ingredient_products = get_product_sets(data)
    for allergen, products_a in allergen_products.items():
        for ingredient, products_i in ingredient_products.items():
            # if the all the products containing this allergen are also found
            # in an ingredient then this ingredient is a possible source for the allergen
            if products_a <= products_i:
                possible[allergen].add(ingredient)
    return possible


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    mappings = get_possibilities(data)
    reduced, mappings = resolve_injective_mappings(mappings)

    if not reduced:
        print("Could not reduce")
        print(mappings)
        return 0

    cnt = 0
    for ingredients, _ in data:
        cnt += len(ingredients.difference(set(mappings.values())))

    return cnt


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    mappings = get_possibilities(data)
    reduced, mappings = resolve_injective_mappings(mappings)

    if not reduced:
        print("Could not reduce")
        print(mappings)
        return 0

    allergens = sorted(mappings)
    ingredients = [mappings[allergen] for allergen in allergens]

    return ",".join(ingredients)


@aoc_part
def solve_part_c(data) -> int:
    """Solve part B"""
    mappings = get_possibilities(data)
    mappings = list(mapping_options(mappings))
    assert len(mappings) == 1
    mappings = mappings[0]
    allergens = sorted(mappings)
    ingredients = [mappings[allergen] for allergen in allergens]

    return ",".join(ingredients)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)

solve_part_c(EX_DATA)
solve_part_c(MY_DATA)
