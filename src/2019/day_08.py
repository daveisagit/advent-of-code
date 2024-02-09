"""Advent of code 2019
--- Day 8: Space Image Format ---
"""

from collections import Counter
from common.aoc import file_to_string, aoc_part, get_filename
from common.general import window_over


IMG_W = 25
IMG_H = 6
LAYER_SZ = IMG_H * IMG_W


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for layer in window_over(raw_data, LAYER_SZ, LAYER_SZ):
        l = []
        for row in window_over(layer, IMG_W, IMG_W):
            row = [int(d) for d in row]
            l.append(row)
        data.append(l)
    return data


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    layer_counts = []
    for layer in data:
        layer_cnt = Counter()
        for row in layer:
            cnt = Counter(row)
            layer_cnt.update(cnt)
        layer_counts.append(layer_cnt)

    zeros = [layer[0] for layer in layer_counts]
    min_zero = min(zeros)
    layer_idx = zeros.index(min_zero)
    cnt = layer_counts[layer_idx]
    return cnt[1] * cnt[2]


def dump_img(img):
    """Visual"""
    for row in img:
        row = ["#" if p == 1 else " " for p in row]
        print("".join(row))


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    final_image = []
    for _ in range(IMG_H):
        row = [2] * IMG_W
        final_image.append(row)

    for layer in data:
        for ri, row in enumerate(layer):
            for ci, pix in enumerate(row):
                if pix == 2:
                    continue
                if final_image[ri][ci] == 2:
                    final_image[ri][ci] = pix

    dump_img(final_image)

    return 0


MY_RAW_DATA = file_to_string(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(MY_DATA)
solve_part_b(MY_DATA)
