"""Advent of code 2017
--- Day 20: Particle Swarm ---
"""

from collections import Counter
from operator import add
import re
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import window_over


def parse_data(raw_data):
    """Parse the input"""
    particles = []
    for line in raw_data:
        result = re.search(
            r"p=<(-?\d+),(-?\d+),(-?\d+)>, v=<(-?\d+),(-?\d+),(-?\d+)>, a=<(-?\d+),(-?\d+),(-?\d+)>",
            line,
        )
        values = [int(v) for v in result.groups()]
        particle = tuple(tuple(t) for t in window_over(values, 3, 3))
        particles.append(particle)

    return particles


def tick(particles):
    """Do a tick"""
    new_states = []
    for p, v, a in particles:
        nv = tuple(map(add, v, a))
        np = tuple(map(add, p, nv))
        new_states.append((np, nv, a))
    return new_states


def manhattan(p):
    """Manhattan"""
    d = 0
    for x in p:
        d += abs(x)
    return d


def p_matches_a(particle):
    """Has the particle resolved direction"""
    p = particle[0]
    a = particle[2]
    matches = True
    for i in range(3):
        if p[i] * a[i] < 0:
            matches = False
            break
    return matches


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    particles = data
    cnt = 0
    while True:
        cnt += 1
        particles = tick(particles)
        matches = [p_matches_a(particle) for particle in particles]
        if all(matches):
            break

    md = [manhattan(p[0]) for p in particles]
    close = min(md)
    closest = [ip for ip, d in enumerate(md) if d == close]
    return closest[0]


def remove_collisions(particles):
    """Boom !"""
    positions = [particle[0] for particle in particles]
    up = set(positions)
    if len(up) == len(positions):
        return particles
    cnt = Counter(positions)
    collisions = [p for p, cnt in cnt.items() if cnt > 1]
    particles = [particle for particle in particles if particle[0] not in collisions]
    return particles


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    particles = data
    cnt = 0
    while True:
        cnt += 1
        particles = tick(particles)
        particles = remove_collisions(particles)
        matches = [p_matches_a(particle) for particle in particles]
        if all(matches):
            break

    return len(particles)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(MY_DATA)
