"""Advent of code 2020
--- Day 20: Jurassic Jigsaw ---
"""

from collections import deque
import math
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import split_into_groups
from common.grid_2d import dihedral_arrangements, get_grid_limits


def parse_data(raw_data):
    """Parse the input"""
    tiles = {}
    for tile in split_into_groups(raw_data, 12):
        tn = int(tile[0][5:9])
        grid = []
        for row in tile[1:11]:
            row = list(row)
            grid.append(row)
        tiles[tn] = grid
    return tiles


def dump_grid(g):
    """Visual"""
    print()
    for row in g:
        print("".join(row))


def encode_sides(g):
    """Return 8 arrangements with sides binary encoded
    An arrangement being (a,b), (N,W,S,E)
    """

    def enc(lst):
        bin_str = "".join(["1" if c == "#" else "0" for c in lst])
        return int(bin_str, 2)

    for a, b, g in dihedral_arrangements(g):
        n = enc(g[0])
        s = enc(g[-1])
        w = [r[0] for r in g]
        w = enc(w)
        e = [r[-1] for r in g]
        e = enc(e)
        yield (a, b), (n, w, s, e)


def encoded_tiles(tiles):
    """Return tile dictionary, where an item is also a dictionary
    keyed on transform with tuple value (N,W,S,E) of encoded sides"""
    enc_tiles = {}
    for tn, tile in tiles.items():
        enc_tile = {}
        for transform, encoding in encode_sides(tile):
            enc_tile[transform] = encoding
        enc_tiles[tn] = enc_tile
    return enc_tiles


def solve_puzzle(data) -> int:
    """find a solution"""
    enc_tiles = encoded_tiles(data)
    total_tiles = len(enc_tiles)
    gs = int(math.sqrt(total_tiles))
    bfs = deque()
    # state is a grid of tiles along with the transform
    # an entry in the list is (tn, transform)
    state = []
    bfs.append(state)

    while bfs:
        state = bfs.pop()
        if len(state) == total_tiles:
            return gs, state

        used_tiles = {tile[0] for tile in state}
        available_tiles = [tn for tn in enc_tiles if tn not in used_tiles]
        tile_place = len(used_tiles)
        for nxt_tile in available_tiles:
            enc_tile = enc_tiles[nxt_tile]
            for transform, encoding in enc_tile.items():
                if tile_place >= gs:
                    above_num, above_transform = state[tile_place - gs]
                    above_encoding = enc_tiles[above_num][above_transform]
                    above_south = above_encoding[2]
                    if encoding[0] != above_south:
                        continue
                if tile_place % gs != 0:
                    left_num, left_transform = state[tile_place - 1]
                    left_encoding = enc_tiles[left_num][left_transform]
                    left_east = left_encoding[3]
                    if encoding[1] != left_east:
                        continue
                new_state = state.copy()
                new_state.append((nxt_tile, transform))
                bfs.append(new_state)

    return None


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    gs, state = solve_puzzle(data)
    return state[0][0] * state[gs - 1][0] * state[gs * (gs - 1)][0] * state[-1][0]


def generate_picture(data):
    """Create the picture"""
    gs, state = solve_puzzle(data)
    ts = len(data[state[0][0]])
    picture = []
    for row_of_tiles in split_into_groups(state, gs):
        for ri in range(1, ts - 1):
            line = []
            for tile_num, transform in row_of_tiles:
                tile = [
                    layout
                    for a, b, layout in dihedral_arrangements(data[tile_num])
                    if (a, b) == transform
                ][0]
                line.extend(tile[ri][1:-1])
            picture.append(line)
    return picture


monster = (
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   ",
)


def grid_to_point_set(g):
    """Return grid as a set of (r,c)"""
    hashes = set()
    for ri, row in enumerate(g):
        for ci, c in enumerate(row):
            if c == "#":
                hashes.add((ri, ci))
    return hashes


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    picture = generate_picture(data)
    hashes = grid_to_point_set(picture)
    _, _, max_r, max_c = get_grid_limits(hashes)
    covered = set()
    for _, _, m in dihedral_arrangements(monster):
        mp = grid_to_point_set(m)
        _, _, max_mr, max_mc = get_grid_limits(mp)
        for ro in range(max_r - max_mr + 1):
            for co in range(max_c - max_mc + 1):
                tmp = {(r + ro, c + co) for r, c in mp}
                if hashes.intersection(tmp) == tmp:
                    covered.update(tmp)

    return len(hashes) - len(covered)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
