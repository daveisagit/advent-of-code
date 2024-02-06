"""Code for solving logic type puzzles"""

from collections import defaultdict


def resolve_injective_mappings(possibilities):
    """Given a dictionary of possible mappings for the key
    It is assumed there is a rule which implies the key can have only 1 value
    If possible return True and a dictionary with a single value based on the inference.

    We can iteratively reduce the possibilities where a key only has 1
    possibility by removing its value from the possibilities of other keys.

    For example
    A: {1,2} B: {2:3} c:{3}
    Would mean c=3 and so B=2 and so A=1

    If we cant completely reduce the mappings then return False and the current map.

    This could go further by looking for pairs and removing them (and triples etc.)
    as you might in a Sudoku but for now singles are enough for AoC
    """

    def resolved_an_inference(current_map):
        reduced = False
        singles = {
            key: list(values)[0]
            for key, values in current_map.items()
            if len(values) == 1
        }
        reduced_map = defaultdict(set)
        for key, values in current_map.items():
            # copy the existing single mappings
            if key in singles:
                reduced_map[key] = {singles[key]}
                continue

            # where there are still multiple
            for value in values:
                # don't copy if a known single value
                if value in singles.values():
                    reduced = True
                    continue
                reduced_map[key].add(value)
        return reduced, reduced_map

    # initialize the current map
    # convert lists and tuples to set
    current_map = defaultdict(set)
    for key, values in possibilities.items():
        if isinstance(values, set):
            current_map[key] = values.copy()
        else:
            current_map[key] = set(values)

    # keep iterating whilst we are making a difference
    reducing = True
    while reducing:
        reducing, current_map = resolved_an_inference(current_map)

    # the injection is the final result
    injection = {
        key: list(values)[0] for key, values in current_map.items() if len(values) == 1
    }

    if len(injection) == len(possibilities):
        return True, injection

    return False, current_map
