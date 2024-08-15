"""Advent of code 2022
--- Day 22: Monkey Map ---
"""

from collections import defaultdict
from copy import deepcopy
from itertools import combinations
from operator import add, sub
from common.grid_2d import directions
from common.aoc import (
    aoc_part,
    file_to_list_rstrip,
    get_filename,
)


def parse_data(raw_data):
    """Parse the input"""
    map = []
    for i, line in enumerate(raw_data):
        if not line:
            break
        map.append(line)

    raw_moves = raw_data[i + 1]
    moves = []
    m = ""
    for ch in raw_moves:
        if ch in "LR":
            if m:
                moves.append(int(m))
                m = ""
            moves.append(ch)
            continue
        m += ch
    moves.append(int(m))

    return map, moves


def map_to_grid(map):
    grid = {}
    start = None
    for r, row in enumerate(map):
        for c, ch in enumerate(row):
            if ch != " ":
                grid[(r, c)] = ch
                if not start and ch != "#":
                    start = (r, c)
    return grid, start


def next_pos(grid, cp, d):
    dv = directions[d]
    np = tuple(map(add, cp, dv))
    r, c = np

    if np not in grid:
        if d in "^v":
            row = [p[0] for p in grid if p[1] == c]
            if d == "^":
                v = max(row)
            else:
                v = min(row)
            np = v, c
        else:
            col = [p[1] for p in grid if p[0] == r]
            if d == "<":
                v = max(col)
            else:
                v = min(col)
            np = r, v

    assert np in grid

    if grid[np] == "#":
        return cp
    return np


def get_passcode(cp, d):
    return (cp[0] + 1) * 1000 + (cp[1] + 1) * 4 + ">v<^".index(d)


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    d_list = list(directions.keys())
    map, moves = data
    grid, cp = map_to_grid(map)
    d = ">"
    for m in moves:
        if isinstance(m, int):
            for _ in range(m):
                cp = next_pos(grid, cp, d)
            continue

        di = d_list.index(d)
        if m == "L":
            di += 1
        else:
            di -= 1
        di %= 4
        d = d_list[di]

    return get_passcode(cp, d)


#
# Remaining code for part B
#


def get_net(grid, face_size):
    """Return a dictionary of faces keyed on the top-left net coordinate where
    values are dicts of directions pointing to edges and a Node graph for all net points.
    Also return a dict of nodes containing a set of faces the node is on
    """
    r = 0
    c = 0
    faces = {}
    node_graph = defaultdict(dict)

    for r in range(6):
        for c in range(6):
            if (r * face_size, c * face_size) in grid:
                face = {
                    "^": ((r, c), (r, c + 1)),
                    "v": ((r + 1, c), (r + 1, c + 1)),
                    "<": ((r, c), (r + 1, c)),
                    ">": ((r, c + 1), (r + 1, c + 1)),
                }
                faces[(r, c)] = face

                p = (r, c)
                x = (r, c + 1)
                y = (r + 1, c)
                z = (r + 1, c + 1)
                node_graph[p][x] = 1
                node_graph[x][p] = 1
                node_graph[p][y] = 1
                node_graph[y][p] = 1
                node_graph[z][x] = 1
                node_graph[x][z] = 1
                node_graph[z][y] = 1
                node_graph[y][z] = 1

    nodes = defaultdict(set)
    for face, edges in faces.items():
        for u, v in edges.values():
            nodes[u].add(face)
            nodes[v].add(face)

    return faces, nodes, node_graph


def make_cube(i_nodes, i_node_graph):
    """Take a list of nodes and their faces with a graph of the net
    and return revised inputs plus a dictionary of merged nodes.
    The 6 faces will form a cube
    """

    def pair_2_nodes(nodes, node_graph, merged_nodes):
        """Look for a node of degree 4 and then select candidates
        from neighbours of degree 3 or less. If a pair of candidates
        are not on the same face or adjacent faces then merge the nodes.
        Do this recursively DFS, to explore all possible ways until a
        valid cube is found."""

        def nodes_on_adjacent_faces():
            a_faces = [f for f in nodes[a]]
            b_faces = [f for f in nodes[b]]
            for fa in a_faces:
                a_nodes = {n for n, nf in nodes.items() if fa in nf}
                for fb in b_faces:
                    b_nodes = {n for n, nf in nodes.items() if fb in nf}
                    common_nodes = a_nodes & b_nodes
                    if len(common_nodes) == 2:
                        return True
            return False

        deg_4 = [u for u, edges in node_graph.items() if len(edges) == 4]
        for u4 in deg_4:
            candidates = [v for v in node_graph[u4] if len(node_graph[v]) < 4]
            if len(candidates) < 2:
                continue
            for a, b in combinations(candidates, 2):

                # ignore if a,b are on the same face
                if nodes[a] & nodes[b]:
                    continue

                # ignore if a,b are on adjacent faces
                if nodes_on_adjacent_faces():
                    continue

                # merge them
                new_merged_nodes = deepcopy(merged_nodes)
                new_merged_nodes[a].update(new_merged_nodes[b])
                del new_merged_nodes[b]

                new_nodes = deepcopy(nodes)
                new_nodes[a].update(new_nodes[b])
                del new_nodes[b]

                new_graph = deepcopy(node_graph)
                for n in new_graph[b]:
                    new_graph[a][n] = 1
                    new_graph[n][a] = 1
                    del new_graph[n][b]
                del new_graph[b]

                if all(len(e) == 3 for e in new_graph.values()) and len(new_graph) == 8:
                    return new_nodes, new_graph, new_merged_nodes

                result = pair_2_nodes(new_nodes, new_graph, new_merged_nodes)
                if result:
                    return result

    merged_nodes = {n: {n} for n in i_nodes}
    return pair_2_nodes(i_nodes, i_node_graph, merged_nodes)


def make_face_grids(grid, faces, face_size):
    """Localized coordinates for each face"""
    face_grids = defaultdict(dict)
    for f in faces:
        offset = tuple(x * face_size for x in f)
        for p, v in grid.items():
            p = tuple(map(sub, p, offset))
            if 0 <= p[0] < face_size and 0 <= p[1] < face_size:
                face_grids[f][p] = v
    return face_grids


def next_face_pos_dir(cf, cp, cd, faces, face_grids, face_size):
    """Get the next face, local position and direction"""
    dv = directions[cd]
    np = tuple(map(add, cp, dv))
    nf = cf
    nd = cd
    grid = face_grids[cf]
    nxt_grid = face_grids[cf]

    if np not in grid:

        # find the matching edge on the cube, check every face
        edge = set(faces[cf][cd])
        for f, es in faces.items():

            # ignore the face we are on
            if f == cf:
                continue

            # search all edges of this face
            for d, e in es.items():

                if set(e) == edge:
                    # edge found, giving the next face and direction
                    nf = f
                    nd = d
                    break

            # if we've changed face then we are done
            if nf != cf:
                break

        # setup the next local grid
        nxt_grid = face_grids[nf]

        # the offset is the amount in from a corner
        # travelling up/down will be the column
        # left/right will be the row
        if cd in "^v":
            offset = cp[1]
        else:
            offset = cp[0]

        # here comes the twist
        # if the node labelling for edge is the reverse
        # then the offset is from the other corner
        if faces[cf][cd] != faces[nf][nd]:
            offset = face_size - offset - 1

        # starting top means travelling down so
        # reverse the new direction to be correct
        nd = "<^>v"[">v<^".index(nd)]

        # now we know the direction we have everything
        # to determine the next local position
        if nd == "^":
            np = (face_size - 1, offset)
        elif nd == "v":
            np = (0, offset)
        elif nd == "<":
            np = (offset, face_size - 1)
        else:
            np = (offset, 0)

    assert np in nxt_grid

    if nxt_grid[np] == "#":
        return cf, cp, cd
    return nf, np, nd


@aoc_part
def solve_part_b(data, face_size=4) -> int:
    """Solve part B"""
    d_list = list(directions.keys())
    puzzle_map, moves = data
    grid, cp = map_to_grid(puzzle_map)

    # get starting face and position
    cf = tuple(x // face_size for x in cp)
    cp = tuple(x % face_size for x in cp)
    cd = ">"

    # work out the net
    faces, nodes, node_graph = get_net(grid, face_size)

    # create localized grids
    face_grids = make_face_grids(grid, faces, face_size)

    # build the cube
    nodes, node_graph, merged_nodes = make_cube(nodes, node_graph)

    # create a map to the surviving nodes
    merged_map = {}
    for n, ms in merged_nodes.items():
        for m in ms:
            merged_map[m] = n

    # re-create the face model referencing the surviving nodes
    new_faces = {}
    for face, edges in faces.items():
        new_edges = {}
        for d, (u, v) in edges.items():
            new_edges[d] = (merged_map[u], merged_map[v])
        new_faces[face] = new_edges

    # traverse the cube
    for m in moves:
        if isinstance(m, int):
            for _ in range(m):
                cf, cp, cd = next_face_pos_dir(
                    cf, cp, cd, new_faces, face_grids, face_size
                )
            continue

        di = d_list.index(cd)
        if m == "L":
            di += 1
        else:
            di -= 1
        di %= 4
        cd = d_list[di]

    cf = tuple(x * face_size for x in cf)
    cp = tuple(map(add, cf, cp))
    return get_passcode(cp, cd)


EX_RAW_DATA = file_to_list_rstrip(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list_rstrip(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA, face_size=50)
