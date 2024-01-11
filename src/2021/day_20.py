"""Advent of code 2021
--- Day 20: Trench Map ---
"""


from common.aoc import ENCODING, dump_path, file_to_list, aoc_part, get_filename
from common.grid_2d import get_grid_limits


def parse_data(raw_data):
    """Parse the input"""

    def to_bin(line):
        return [c == "#" for c in line]

    image = set()
    eas = to_bin(raw_data[0])
    for ri, line in enumerate(raw_data[2:]):
        for ci, c in enumerate(line):
            if c == "#":
                image.add((ri, ci))

    return image, eas


def iterate(image, eas, infinity=0):
    """Iterate"""

    # If ehe EAS has # for EAS[0] and . for EAS[511] then infinity
    # will look like . on even and # on odd iterations
    def fill(r, c):
        w = []
        for rw in range(-1, 2):
            for cw in range(-1, 2):
                r2 = r + rw
                c2 = c + cw
                # for an odd iteration we will need to fill the gaps with 1s
                # when outside our image boundary
                if infinity and (r2 < min_r or r2 > max_r or c2 < min_c or c2 > max_c):
                    w.append("1")
                    continue
                if (r2, c2) in image:
                    w.append("1")
                    continue
                w.append("0")
        v = int("".join(w), 2)
        return eas[v]

    new_image = set()
    min_r, min_c, max_r, max_c = get_grid_limits(image)
    for r in range(min_r - 1, max_r + 2):
        for c in range(min_c - 1, max_c + 2):
            if fill(r, c):
                new_image.add((r, c))
    return new_image


def dump_image(image, margin=0):
    """Visual"""
    print()
    min_r, min_c, max_r, max_c = get_grid_limits(image)
    for r in range(min_r - margin, max_r + margin + 1):
        row = []
        for c in range(min_c - margin, max_c + margin + 1):
            if (r, c) in image:
                row.append("#")
            else:
                row.append(".")
        print("".join(row))


def dump_image_to_file(image, margin=0):
    """Visual to file"""
    fn = dump_path(__file__)
    with open(fn, encoding=ENCODING, mode="w") as f:
        min_r, min_c, max_r, max_c = get_grid_limits(image)
        for r in range(min_r - margin, max_r + margin + 1):
            row = []
            for c in range(min_c - margin, max_c + margin + 1):
                if (r, c) in image:
                    row.append("#")
                else:
                    row.append(".")
            f.write("".join(row) + "\n")


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    img, eas = data
    infinity_flips = eas[0]
    infinity = 0
    if infinity_flips:
        infinity = 1
    img = iterate(img, eas)
    img = iterate(img, eas, infinity)
    return len(img)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    img, eas = data
    infinity_flips = eas[0]
    for i in range(50):
        img = iterate(img, eas, i % 2 if infinity_flips else 0)
    # dump_image_to_file(img)
    return len(img)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
