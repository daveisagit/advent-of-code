"""Advent of code 2021
--- Day 13: Transparent Origami ---
"""

from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok
from common.grid_2d import XY, get_grid_limits


def parse_data(raw_data):
    """Parse the input"""
    coords = []
    folds = []
    for ln, line in enumerate(raw_data):
        if not line:
            break
        arr = tok(line, delim=",")
        coords.append(XY(int(arr[0]), int(arr[1])))

    for line in raw_data[ln + 1 :]:
        arr = tok(line, delim="=")
        fold = (arr[0][-1], int(arr[1]))
        folds.append(fold)

    return coords, folds


def update_with_fold(dots: set, fold):
    """Updates the set of dots after a fold has been made"""

    axis = fold[0]
    idx = fold[1]

    # remove ones on the fold line
    if axis == "x":
        dots_on_fold = {d for d in dots if d.x == idx}
    if axis == "y":
        dots_on_fold = {d for d in dots if d.y == idx}
    dots.difference_update(dots_on_fold)

    # get the dots on the higher side
    if axis == "x":
        higher_dots = {d for d in dots if d.x > idx}
    if axis == "y":
        higher_dots = {d for d in dots if d.y > idx}

    # remove them from dots
    dots.difference_update(higher_dots)

    # transpose higher dots to new post-fold coordinates
    if axis == "x":
        reflected = {XY(2 * idx - d.x, d.y) for d in higher_dots}
    if axis == "y":
        reflected = {XY(d.x, 2 * idx - d.y) for d in higher_dots}

    dots.update(reflected)


def dump_dots(dots):
    """Visualize the dots"""
    min_x, min_y, max_x, max_y = get_grid_limits(dots)

    row = ["."] * (max_x - min_x + 1)
    grid = []
    for _ in range(min_y, max_y + 1):
        grid.append(row.copy())

    for dot in dots:
        grid[dot.y][dot.x] = "#"

    for row in grid:
        row = "".join(row)
        print(row)


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    coords = data[0]
    folds = data[1]
    dots = set(coords)
    update_with_fold(dots, folds[0])
    return len(dots)


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    coords = data[0]
    folds = data[1]
    dots = set(coords)
    for fold in folds:
        update_with_fold(dots, fold)
    dump_dots(dots)
    return "captcha!"


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
