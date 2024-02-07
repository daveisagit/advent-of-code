"""Advent of code 2020
--- Day 24: Lobby Layout ---
"""

from collections import defaultdict
from operator import add
from common.aoc import file_to_list, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        tile = []
        while line:
            if line[0] in ("sn"):
                tile.append(line[:2])
                line = line[2:]
            else:
                tile.append(line[:1])
                line = line[1:]
        data.append(tile)
    return data


hex_map = {
    "e": (2, 0),
    "ne": (1, 1),
    "nw": (-1, 1),
    "w": (-2, 0),
    "sw": (-1, -1),
    "se": (1, -1),
}


def get_tile_visits(data):
    """Return a dict of hex co-ord, value is number of visits"""
    tile_count = defaultdict(int)
    for tile in data:
        tile_map = [hex_map[d] for d in tile]
        loc = (0, 0)
        for tm in tile_map:
            loc = tuple(map(add, loc, tm))
        tile_count[loc] += 1
    return tile_count


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    tile_count = get_tile_visits(data)
    res = sum(cnt % 2 for cnt in tile_count.values())
    return res


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""

    def iterate(tiles):

        # establish a rough border
        min_re = min(re for re, im in tiles)
        max_re = max(re for re, im in tiles)
        min_im = min(im for re, im in tiles)
        max_im = max(im for re, im in tiles)

        new_layout = set()
        for re in range(min_re - 1, max_re + 2):
            for im in range(min_im - 1, max_im + 2):
                tile = (re, im)
                tc = 0
                if tile in tiles:
                    tc = 1

                bn = 0
                for d in hex_map.values():
                    loc = tuple(map(add, tile, d))
                    if loc in tiles:
                        bn += 1

                if tc == 1:
                    if bn == 0 or bn > 2:
                        tc = 0
                if tc == 0:
                    if bn == 2:
                        tc = 1

                if tc == 1:
                    new_layout.add(tile)

        return new_layout

    tiles = get_tile_visits(data)
    tiles = {t for t, v in tiles.items() if (v % 2) == 1}

    for _ in range(100):
        tiles = iterate(tiles)

    res = len(tiles)

    return res


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
