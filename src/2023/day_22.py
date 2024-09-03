"""Advent of code 2023
--- Day 22: Sand Slabs ---
"""

from collections import defaultdict, deque
from copy import deepcopy
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""

    def normalise(block):
        """Represent a block consistently a -> b in all directions
        and a <= space < b"""
        a, b = block
        na = []
        nb = []
        for i in range(len(a)):
            ai = a[i]
            bi = b[i]
            nai = min(ai, bi)
            nbi = max(ai, bi)
            na.append(nai)
            nb.append(nbi)

        # like python ranges, have the upper limit exclusive
        nb = [x + 1 for x in nb]
        return tuple(na), tuple(nb)

    blocks = []
    for line in raw_data:
        arr = tok(line, "~")
        block = tuple(tuple(int(x) for x in tok(blk, ",")) for blk in arr)
        blocks.append(normalise(block))

    # make sure we process them in the order they were given in the snapshot
    blocks = sorted([b for b in blocks], key=lambda x: x[0][2])

    return blocks


def intersects(a, b):
    """Return True if these blocks overlap at all"""
    for i in range(3):
        ai = max(a[0][i], b[0][i])
        bi = min(a[1][i], b[1][i])
        if bi <= ai:
            return False
    return True


def get_support_dependencies(blocks):
    """Return a list of supporting dependencies
    each as a tuple (supporting block, supported block)
    each as an index from the blocks list
    """
    landed = []
    support_dependencies = []
    top_of_stack = 0
    at_height = defaultdict(set)
    for block_idx, block in enumerate(blocks):

        # make the block mutable
        block = [list(corner) for corner in block]

        # place it just above the landed stack
        top_of_stack = max([b[1][2] for b in landed], default=0)
        height = block[1][2] - block[0][2]
        block[0][2] = top_of_stack
        block[1][2] = top_of_stack + height

        # start the decent until we hit another landed block
        # or the floor
        while block[0][2] >= 0:
            block[0][2] -= 1
            block[1][2] -= 1
            stop = False
            # check all the landed blocks that exist at this height
            for landed_idx in at_height[block[0][2]]:
                landed_block = landed[landed_idx]
                if intersects(block, landed_block):
                    # note all the supporting dependencies
                    # and we need go no further in the decent
                    support_dependencies.append((landed_idx, block_idx))
                    stop = True
            if stop:
                break

        # come back 1 level, since we collided on this one
        block[0][2] += 1
        block[1][2] += 1

        # add to the landed list
        landed.append(block)

        # note the heights it covers, this for an optimisation
        # in the search above to save us checking all landed blocks
        for h in range(block[0][2], block[1][2]):
            at_height[h].add(block_idx)

    return support_dependencies


def safely_remove(blocks, support_dependencies):
    remove = set()
    supported_blocks = {b for _, b in support_dependencies}
    for idx in range(len(blocks)):
        # compare the remaining blocks after removing a support
        remain = {b for a, b in support_dependencies if a != idx}
        if supported_blocks == remain:
            remove.add(idx)
    return remove


@aoc_part
def solve_part_a(blocks) -> int:
    """Solve part A"""
    support_dependencies = get_support_dependencies(blocks)
    return len(safely_remove(blocks, support_dependencies))


@aoc_part
def solve_part_b(blocks) -> int:
    """Solve part B"""

    def get_remains(remove):
        """Remove edges from the dag that point to the given block
        if that leaves a node with no edges then it is unsupported
        and should also be removed.
        Return what remains
        """
        dag = deepcopy(depends_on_dag)
        q = deque()
        q.append(remove)
        while q:
            rmv = q.popleft()
            for di in list(dag.keys()):
                dag[di].discard(rmv)
                if dag[di]:
                    continue
                del dag[di]
                q.append(di)
        return dag

    support_dependencies = get_support_dependencies(blocks)
    supported = {b for _, b in support_dependencies}

    # create a dag to model the blocks as a set that support a given block
    # we add the floor as -1 to represent the floor for such blocks
    # not supported by another block
    depends_on_dag = defaultdict(set)
    for a, b in support_dependencies:
        depends_on_dag[b].add(a)
    for i in range(len(blocks)):
        if i not in supported:
            depends_on_dag[i].add(-1)

    # only need to process the blocks that can not be safely removed
    blocks_to_remove = set(range(len(blocks))) - safely_remove(
        blocks, support_dependencies
    )
    print(f"Blocks not safe to remove: {len(blocks_to_remove)}")

    return sum(len(blocks) - len(get_remains(i)) for i in blocks_to_remove)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
