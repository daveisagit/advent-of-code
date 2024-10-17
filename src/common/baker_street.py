from collections import defaultdict
from itertools import pairwise
from common.general import tok
from common.graph import get_adjacency_matrix, merge_nodes_keep_first, optimal_route
from common.grid_2d import maze_to_graph
from pyvis.network import Network

board = """
....xxx9........9xx...
....x.......9.....x...
....x.......x.....x...
..Dxxxxxxxxxxxxxxxx...
....x...x....x....xF..
....x...3....5....x...
....x.............x...
.2..x.............x...
.x..x.............x...
xxxxxxxxxxxxxxxxxxxx1.
x.....x...x..x....x...
x.....x...B..x....x...
x...7xx......x....x...
x.....x......xxE..xx8.
x.....x......x....x...
x.....x......x....x...
xxxxxxxxxxxxxxxxxxxx..
..x.....x......x...x..
..4.....x......A...x..
........x..........x..
........x..C.......xx6
........x..x.......x..
......4xxxxxxxxxxxxx..
......................
"""

locations_names = """
1 Chemist
2 Bank
3 Carriage Depot
4 Docks
5 Hotel
6 Locksmith
7 Museum
8 Newsagent
9 Park
A Pawnbroker
B Theatre
C Boars Head
D Scotland Yard
E Tobacconists
F Baker street
"""


def parse_data():
    locations = {}
    grid_locations = {}
    for line in locations_names.splitlines()[1:]:
        if not line:
            continue
        locations[line[0]] = line[2:]

    grid = {}
    content_filter = set(locations)
    content_filter.add("x")
    for ri, row in enumerate(board.splitlines()[1:]):
        for ci, content in enumerate(row):
            if content not in content_filter:
                continue
            p = (ri, ci)
            grid[p] = content
            if content in locations:
                grid_locations[p] = content
    return locations, grid, grid_locations


def visualize_graph(gph):
    """Basic visual"""
    net = Network(height="1200px", width="100%", directed=True)
    net.show_buttons()

    for n in gph:
        net.add_node(n)

    for u, edges in gph.items():
        for v, c in edges.items():
            print(c)
            net.add_edge(u, v, weight=1, label=str(c))

    # net.toggle_physics(True)
    net.show("temp_graph.html", notebook=False)


def best_route():
    locations, grid, grid_locations = parse_data()
    start = [p for p, c in grid.items() if c == "F"][0]
    path_chars = set(locations)
    path_chars.add("x")
    gph = maze_to_graph(start, grid, path_char=path_chars)

    for loc in locations:
        loc_points = [p for p, n in grid_locations.items() if n == loc]
        if len(loc_points) < 2:
            continue
        for b in loc_points[1:]:
            merge_nodes_keep_first(gph, loc_points[0], b)

    ng = defaultdict(dict)
    for a, e in gph.items():
        for b, w in e.items():
            a2 = grid_locations.get(a, str(a))
            b2 = grid_locations.get(b, str(b))
            ng[a2][b2] = w

    for loc in locations:
        if loc == "3":
            continue
        ng["3"][loc] = 1

    visualize_graph(ng)

    # print(ng)
    r = optimal_route(ng, set(locations), start="F", end="F")
    print(r)
    for l in r[1]:
        print(locations[l])


best_route()
