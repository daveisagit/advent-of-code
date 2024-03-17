"""Advent of code 2018
--- Day 17: Reservoir Research ---
"""

from operator import add
import re
from sys import setrecursionlimit
from common.aoc import dump_path, file_to_list, aoc_part, get_filename, ENCODING
from common.grid_2d import get_grid_limits

setrecursionlimit(3000)

directions = ((0, 1), (-1, 0), (1, 0))


def parse_data(raw_data):
    """Parse the input"""
    walls = set()
    for line in raw_data:
        result = re.search(r"(x|y)=(\d+),\s(x|y)=(\d+)..(\d+)", line)
        d1 = result.group(1)
        v1 = int(result.group(2))
        v2a = int(result.group(4))
        v2b = int(result.group(5))
        for r in range(v2a, v2b + 1):
            if d1 == "x":
                w = (v1, r)
            else:
                w = (r, v1)
            walls.add(w)

    return walls


def draw(walls, still, flowing, focus=None):
    """Visual"""
    min_x, min_y, max_x, max_y = get_grid_limits(walls)
    if focus:
        min_x, min_y, max_x, max_y = focus
    for y in range(min_y, max_y + 1):
        row = ["."] * (max_x - min_x + 1)
        for i, x in enumerate(range(min_x, max_x + 1)):
            p = (x, y)
            if p in walls:
                row[i] = "#"
            if p in still:
                row[i] = "~"
            if p in flowing:
                row[i] = "|"
            if p in still and p in flowing:
                row[i] = "?"

        print("".join(row))


def dump(walls, still, flowing, focus=None):
    """Visual"""
    fn = dump_path(__file__)
    min_x, min_y, max_x, max_y = get_grid_limits(walls)
    if focus:
        min_x, min_y, max_x, max_y = focus
    min_x = min_x - 5
    max_x = max_x + 5
    min_y = 0
    max_y = max_y + 5
    with open(fn, encoding=ENCODING, mode="w") as f:
        for y in range(min_y, max_y + 1):
            row = ["."] * (max_x - min_x + 1)
            for i, x in enumerate(range(min_x, max_x + 1)):
                p = (x, y)
                if p in walls:
                    row[i] = "#"
                if p in still:
                    row[i] = "~"
                if p in flowing:
                    row[i] = "|"
                if p in still and p in flowing:
                    row[i] = "?"

            f.write("".join(row) + "\n")


def run_tap(walls, spring=(500, 0)):
    """Return a set of still and flowing"""

    def plot_droplet(pos, d=0):
        flowing.add(pos)

        # First priority is to go down until we hit something or go too far
        down = tuple(map(add, pos, directions[0]))
        if (
            down not in walls
            and down not in flowing
            and down not in still
            and down[1] <= y_limit
        ):
            # nothing in the way carry on the downward recurrence
            plot_droplet(down)

        # Now we must see if we should carry on or not
        # If the next downward place is in a flow
        # then we need not go any further another droplet has already travelled this path
        # Or, we might be beyond the limit
        # Either way we should just quit the recursion
        if down in flowing or down[1] > y_limit:
            return False

        # The droplet has reach a hard(ish) landing (either wall or still)
        # So now we explore sideways to see if there are walls both sides causing
        # the water to the still.
        # The recurrence returns True if the neighbour should be still (from hitting a wall)
        # No need to recur if we know that side is already in flow

        # left recurrence
        left = tuple(map(add, pos, directions[1]))
        left_still = left in walls or left not in flowing and plot_droplet(left, d=1)

        # right recurrence
        right = tuple(map(add, pos, directions[2]))
        right_still = (
            right in walls or right not in flowing and plot_droplet(right, d=2)
        )

        # if we are between 2 sets of still water then we are still as well
        # and any flowing places beside us are also still
        # remove the newly acquired still from flowing
        if d == 0 and left_still and right_still:
            still.add(pos)
            flowing.discard(pos)
            while left in flowing:
                still.add(left)
                flowing.discard(left)
                left = tuple(map(add, left, directions[1]))

            while right in flowing:
                still.add(right)
                flowing.discard(right)
                right = tuple(map(add, right, directions[2]))

        # Return True if our direction of exploration results in still water
        return d == 1 and left_still or d == 2 and right_still

    _, _, _, y_limit = get_grid_limits(walls)
    flowing = set()
    still = set()

    plot_droplet(spring)

    return still, flowing


@aoc_part
def solve_part_a(walls) -> int:
    """Solve part A"""
    still, flowing = run_tap(walls)
    # dump(walls, still, flowing)

    _, min_y, _, max_y = get_grid_limits(walls)
    all_water = still | flowing
    all_water = {w for w in all_water if min_y <= w[1] <= max_y}

    return len(all_water)


@aoc_part
def solve_part_b(walls) -> int:
    """Solve part B"""
    still, _ = run_tap(walls)
    return len(still)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)


solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
