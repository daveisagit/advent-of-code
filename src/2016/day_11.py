"""Advent of code 2016
--- Day 11: Radioisotope Thermoelectric Generators ---
"""

from collections import defaultdict, deque
from itertools import combinations
import re
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input, floors = 0-3"""
    elements = defaultdict(dict)
    for f, line in enumerate(raw_data):
        arr = tok(line, "contains")
        contents = arr[1]
        if contents[:7] == "nothing":
            continue
        arr = re.split(r",|, and", contents[:-1])
        for c in arr:
            c = c.strip()
            rr = re.search(r"a (.+)( generator|-compatible microchip)", c)
            if rr.group(2)[0] == " ":
                elements[rr.group(1)]["G"] = f
            if rr.group(2)[0] == "-":
                elements[rr.group(1)]["M"] = f

    return elements


def create_initial_state(elements):
    """Items locations in a flat tuple (G1, G2 , ... , Gn , M1, M2, ..., Mn)"""
    e_index = []
    gen_loc = []
    chip_loc = []
    for e, loc in elements.items():
        e_index.append(e)
        gen_loc.append(loc["G"])
        chip_loc.append(loc["M"])

    return tuple(e_index), tuple(gen_loc + chip_loc)


def get_state_key(state):
    """Multiple types with matching G/M on the same floor (as per part B initial state)
    are really the same state, so we can reduce what we check by not exploring the similar state
    for another chip. This reduces part B from 6mins to 1.5s !!!
    """
    lift, locations = state
    sz = len(locations) // 2
    locations = tuple(sorted((locations[i], locations[i + sz]) for i in range(sz)))
    return lift, locations


def solve(elements) -> int:
    """Solve"""
    data = create_initial_state(elements)
    max_floor = 3
    elements, locations = data
    sz = len(elements)
    final = (max_floor, (max_floor,) * sz * 2)

    lift = 0
    state = (lift, locations)
    bfs = deque()
    best_for_state = {}
    bfs.append((state, 0))
    while bfs:
        state, steps = bfs.popleft()
        state_key = get_state_key(state)

        if state == final:
            return steps

        if state_key in best_for_state and best_for_state[state_key] <= steps:
            continue
        best_for_state[state_key] = steps

        lift, locations = state
        generators = locations[:sz]
        chips = locations[sz:]

        # validate state
        valid = True
        for i in range(sz):
            if chips[i] == generators[i]:
                # chip & gen are on the same floor, ok
                continue
            generators_on_this_floor = [x for x in generators if x == chips[i]]
            if generators_on_this_floor:
                valid = False
                break

        if not valid:
            continue

        # options
        for d in range(-1, 2, 2):

            new_lift = lift + d
            if not 0 <= new_lift <= max_floor:
                continue

            on_this_floor = [i for i, x in enumerate(locations) if x == lift]

            # take 1
            for x in on_this_floor:
                new_locations = list(locations)
                new_locations[x] = new_lift
                new_state = (new_lift, tuple(new_locations))
                bfs.append((new_state, steps + 1))

            # take 2
            for a, b in combinations(on_this_floor, 2):
                new_locations = list(locations)
                new_locations[a] = new_lift
                new_locations[b] = new_lift
                new_state = (new_lift, tuple(new_locations))
                bfs.append((new_state, steps + 1))

    return None


@aoc_part
def solve_part_a(elements) -> int:
    """Solve part A"""
    return solve(elements)


@aoc_part
def solve_part_b(elements) -> int:
    """Solve part B"""
    elements["elerium"] = {"M": 0, "G": 0}
    elements["dilithium"] = {"M": 0, "G": 0}
    return solve(elements)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(MY_DATA)
