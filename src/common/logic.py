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


def exact_cover(X, Y):
    """We are looking for any Y* ⊂ Y such that Y* partitions X"""
    X = transform_X_constraints(X, Y)
    for solution in alg_x(X, Y, []):
        yield solution


def transform_X_constraints(X, Y):
    """Transforming the input for the constraints(X) from a set/list to a dict

    We are given the possibilities(Y) as a dict where the values are a collection of
    constraints, each constraint being satisfied by the possibility i ∈ Y.

    In transforming X to a dict the value is the cross ref mapping
    set of possibilities that meet the constraint j in X
    """
    X = {j: set() for j in X}
    for i, row in Y.items():
        for j in row:
            X[j].add(i)
    return X


def alg_x(X, Y, solution):
    """Find solutions to the exact cover using Algorithm X

    We are looking for any Y* ⊂ Y such that Y* partitions X

    Args:
        X (dict):   Constraints and for each the Possibilities meeting it
        Y (dict):   Possibilities and for each the Constraints it satisfies
        solution (list): The current partial solution within the recursion

    Yields:
        A solution

    Domino usage
    X: Dominoes (and for each the set of squares they feature in)
    Y: Squares  (and for each the dominoes they use)
    |X| = 28
    |Y| = 1037


    Sodoku usage
    X: Constraints   (and for each the set of Possibilities they meet)
    Y: Possibilities (and for each the set of Constraints they satisfy)
    |X| = 4 x 81 = 384 (every cell filled, every row has every value, every col has every value, every box etc.)
    |Y| = 9 x 9 x 9 = 729 (every value in every cell)

    """
    if not X:
        # Step 1 - We have a valid solution
        yield list(solution)
    else:
        # Step 2 - choose the column with the fewest ones
        c = min(X, key=lambda c: len(X[c]))

        # Step 3 - for each possibility(r) that meets this constraint(c)
        for r in list(X[c]):

            # Step 4 - add it to the current solution being built
            solution.append(r)

            # Step 5 - note the columns we removed in cols
            cols = select(X, Y, r)

            # Step 6 - repeat recursively
            for s in alg_x(X, Y, solution):
                yield s

            # Our implementation needs to restore X and the current partial
            # solution to what it was before going down a level
            deselect(X, Y, r, cols)
            solution.pop()


def select(X, Y, r):
    """Remove the rows and columns as in Step 5"""
    cols = []
    # for every constraint(j) matching the given possibility(r)
    # i.e. for every column with a 1 in the given row(r)
    for j in Y[r]:

        # for possibility(i) meeting the constraint(j)
        # i.e. for every row with a 1 in this column(j)
        for i in X[j]:

            # for every constraint(k) matching the given possibility(i)
            # i.e. for every column with a 1 in the given row(i)
            for k in Y[i]:

                # Step 5.1.1
                # only to do this if not the same constraint
                # remove the row/possibilities where A(i,j) = 1
                if k != j:
                    X[k].remove(i)

        # Step 5.1
        # remove the column/constraint
        cols.append(X.pop(j))
    return cols


def deselect(X, Y, r, cols):
    """Using the saved cols put things back as they were"""
    for j in reversed(Y[r]):
        X[j] = cols.pop()
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].add(i)


def mapping_options(mapping_constraints: dict):
    """Given a set of mapping constraints for each key as a set of values

    Use the exact covering algorithm to generate all possible mappings that
    would meet the given constraints

    For example
    A: {1,2} B: {2:3} C:{3}
    Would mean C=3 and so B=2 and so A=1 returning just {A:1, B:2, C:3}
    """
    values = set()
    for s in mapping_constraints.values():
        values |= s

    # Build the Constraints (X)
    # every key and value accounted for
    constraints = [("k", k) for k in mapping_constraints] + [("v", v) for v in values]

    possibilities = {}
    for k, s in mapping_constraints.items():
        # each possibility meets name constraint and an index constraint
        for v in s:
            possibilities[(k, v)] = [("k", k), ("v", v)]

    # Yield every possible mapping that meets the constraints
    for solution in exact_cover(constraints, possibilities):
        mapping = {k: v for k, v in solution}
        yield mapping
