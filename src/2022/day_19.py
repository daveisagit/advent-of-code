"""Advent of code 2022
--- Day 19: Not Enough Minerals ---
"""

from collections import deque
from math import prod
from operator import add, sub
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok

MINERALS = ("ore", "clay", "obsidian", "geode")


def parse_data(raw_data):
    """Parse the input"""
    blue_prints = []
    for line in raw_data:
        line = tok(line, ":")[1]
        costings = tok(line, ".")
        costs = []
        for costing in costings:
            if not costing:
                continue
            costing = tok(costing, "costs")[1]
            makeup = tok(costing, "and")
            cost = [0] * 4
            for component in makeup:
                arr = tok(component)
                amt = int(arr[0])
                mineral = MINERALS.index(arr[1])
                cost[mineral] = amt
            costs.append(tuple(cost))
        blue_prints.append(tuple(costs))

    return blue_prints


def tri(n):
    return n * (n + 1) // 2


def most_geode_for_minutes(blueprint, total_time=24):
    minerals = 0, 0, 0, 0
    robots = 1, 0, 0, 0
    state = 0, robots, minerals
    bfs = deque()
    seen = set()
    bfs.append(state)
    most_geode = 0

    # what is the most we could spend of a given mineral in a round
    max_spend = [max(col) for col in zip(*[costs for costs in blueprint])]

    while bfs:
        state = bfs.pop()
        time, robots, minerals = state
        if time >= total_time:
            most_geode = max(most_geode, minerals[3])
            continue

        # make the state green, which acts as a way to prune
        # if our state has excess then reduce it
        time_left = total_time - time
        robots = list(robots)
        minerals = list(minerals)
        for i in range(3):
            # there is no point in having more robots than this as you won't
            # be able to spend it. It will just create excess waste
            if robots[i] >= max_spend[i]:
                robots[i] = max_spend[i]
            # having too much which can not be spent is also waste
            if minerals[i] >= time_left * max_spend[i] - robots[i] * (time_left - 1):
                minerals[i] = time_left * max_spend[i] - robots[i] * (time_left - 1)
        robots = tuple(robots)
        minerals = tuple(minerals)
        state = time, robots, minerals

        if state in seen:
            continue
        seen.add(state)

        # is it worth it?
        max_possible_geodes = tri(robots[3] + time_left) - tri(robots[3]) + minerals[3]
        if most_geode and max_possible_geodes < most_geode:
            continue

        # no build
        new_minerals = tuple(map(add, minerals, robots))
        state = time + 1, robots, new_minerals
        bfs.append(state)

        # with a build
        for ri, costs in enumerate(blueprint):
            if all(costs[i] <= amt for i, amt in enumerate(minerals)):
                new_robots = list(robots)
                new_robots[ri] += 1
                new_minerals = tuple(map(sub, minerals, costs))
                new_minerals = tuple(map(add, new_minerals, robots))
                state = time + 1, tuple(new_robots), tuple(new_minerals)
                bfs.append(state)

    return most_geode


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    return sum(
        (bi + 1) * most_geode_for_minutes(blueprint, total_time=24)
        for bi, blueprint in enumerate(data)
    )


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    data = data[:3]
    return prod(most_geode_for_minutes(blueprint, total_time=32) for blueprint in data)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
