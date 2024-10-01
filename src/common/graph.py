"""Graphing tools"""

from collections import defaultdict, deque
from copy import deepcopy
from heapq import heappop, heappush
from itertools import count
from math import inf

from common.general import tok
from common.heap import BinaryHeap

# Adjacency
#   get_adjacency_matrix:   uses Dijkstra (& options)
#   floyd_warshall:         cross-product of all nodes in a the graph

# Shortest Paths
#   Dijkstra        2 functions one for distances and one for the path too
#   Bellman-Ford:   -ve & disjoint ssc, just distances
#   TSP:            optimal_route() options for visit, start, end (& ignore node callable)

# Longest Path
#   simple recursion (not LRU) using a mutable set for visited

# Minimal Spanning Tree
#   undirected: Prim
#   directed:   Edmonds/Chi
#               Kruskal

# Maximum Spanning Tree
#   directed:   Kruskal, negate the weights

# Flow
#   Edmonds-Karp: TODO: https://en.wikipedia.org/wiki/Edmonds%E2%80%93Karp_algorithm


def all_nodes(gph):
    """Return all the nodes of a graph as a set"""
    nodes = set()
    for u, v in gph.items():
        nodes.add(u)
        nodes.update(v.keys())
    return nodes


#
# SHORTEST PATHS
#


def dijkstra(gph, source, target, weight_attr=None):
    """Uses Dijkstra's algorithm to find shortest path from source -> target
    If no specific target given then return them all"""
    push = heappush
    pop = heappop
    dist = {}  # dictionary of final distances
    seen = {}
    # fringe is heapq with 3-tuples (distance,c,node)
    # use the count c to avoid comparing nodes (may not be able to)
    c = count()
    fringe = []
    seen[source] = 0
    push(fringe, (0, next(c), source))
    while fringe:
        (d, _, v) = pop(fringe)
        if v in dist:
            continue  # already searched this node.
        dist[v] = d
        if v == target:
            break
        for u, attrs in gph[v].items():
            cost = attrs
            if weight_attr:
                cost = attrs[weight_attr]
            vu_dist = dist[v] + cost

            if u not in seen or vu_dist < seen[u]:
                seen[u] = vu_dist
                push(fringe, (vu_dist, next(c), u))

    if target:
        if target in dist:
            return dist[target]
        return None
    return dist


def dijkstra_paths(gph, source, target=None, weight_attr=None):
    """Uses Dijkstra's algorithm to find shortest path from source -> target
    If no specific target given then return them all"""
    push = heappush
    pop = heappop
    dist = {}  # dictionary of final distances
    seen = {}
    paths = {source: [source]}
    # fringe is heapq with 3-tuples (distance,c,node)
    # use the count c to avoid comparing nodes (may not be able to)
    c = count()
    fringe = []
    seen[source] = 0
    push(fringe, (0, next(c), source))
    while fringe:
        (d, _, v) = pop(fringe)
        if v in dist:
            continue  # already searched this node.
        dist[v] = d
        if v == target:
            break
        for u, attrs in gph[v].items():
            cost = attrs
            if weight_attr:
                cost = attrs[weight_attr]
            vu_dist = dist[v] + cost

            if u not in seen or vu_dist < seen[u]:
                seen[u] = vu_dist
                push(fringe, (vu_dist, next(c), u))
                paths[u] = paths[v] + [u]

    if target:
        return dist[target], paths[target]
    return dist, paths


def bellman_ford(graph, source):
    """Like Dijkstra but will handle negative weights"""
    # Step 1: Initialize distances
    distances = {n: inf for n in all_nodes(graph)}
    distances[source] = 0

    # Step 2: Relax edges |V| - 1 times
    for _ in range(len(graph) - 1):
        for u in graph:
            for v, weight in graph[u].items():
                if distances[u] != inf and distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight

    # Step 3: Check for negative weight cycles
    for u in graph:
        for v, weight in graph[u].items():
            if distances[u] != inf and distances[u] + weight < distances[v]:
                raise ValueError("Graph contains negative weight cycle")

    return distances


def get_longest_path(gph, start, finish):
    """Return the longest path length between start and finish that visits nodes
    only once (not all nodes need to be visited)"""

    def longest(cur, dst, best):
        if cur == finish:
            return dst
        if cur in seen:
            return best
        # it is more efficient to keep a mutable set maintained
        # rather than passing a new frozen one in the arguments
        seen.add(cur)
        best = max(longest(nxt, d + dst, best) for nxt, d in gph[cur].items())
        seen.remove(cur)
        return best

    seen = set()

    return longest(start, 0, 0)


def simplify(gph, protected_nodes=None):
    """
    Remove nodes and merge edges for nodes with 2 edges
    assumes single attr of cost"""
    if protected_nodes is None:
        protected_nodes = {}
    candidates = {u for u, oe in gph.items() if len(oe) == 2}
    candidates.difference_update(protected_nodes)
    while candidates:
        n = list(candidates)[0]
        e_sum = sum(gph[n].values())
        neighbours = list(gph[n].keys())
        if len(neighbours) != 2:
            raise RuntimeError("WHAT")
        u = neighbours[0]
        v = neighbours[1]
        del gph[n][u]
        del gph[n][v]
        del gph[u][n]
        del gph[v][n]
        if u in gph and v in gph[u]:
            e_sum = min(e_sum, gph[u][v])
        gph[u][v] = e_sum
        gph[v][u] = e_sum
        del gph[n]
        candidates = {u for u, oe in gph.items() if len(oe) == 2}
        candidates.difference_update(protected_nodes)


# For Adjacency Matrix:
# Run Dijkstra from all nodes if you expect to have about as many
# edges as you have nodes, and run Floyd if you expect to have almost complete
# graphs.


def get_adjacency_matrix(
    gph, nodes=None, weight_attr=None, include_unreachable=False, include_diagonal=False
):
    """Returns the adjacency matrix (as dict)"""
    matrix = {}
    if nodes is None:
        nodes = all_nodes(gph)

    if include_unreachable:
        for u in nodes:
            matrix[u] = {}
            for v in nodes:
                matrix[u][v] = inf
                if u == v and include_diagonal:
                    matrix[u][v] = 0

    for u in nodes:
        distances, _ = dijkstra_paths(gph, u, weight_attr=weight_attr)
        if not include_unreachable:
            matrix[u] = {}
        for v, d in distances.items():
            if u == v:
                if include_diagonal:
                    matrix[u][v] = 0
                continue
            if v not in nodes:
                continue
            matrix[u][v] = d
    return matrix


def floyd_warshall(gph):
    """Returns the adjacency matrix (as dict)"""
    matrix = defaultdict(dict)
    nodes = all_nodes(gph)
    for u in nodes:
        for v in nodes:
            matrix[u][v] = inf
            if u == v:
                matrix[u][v] = 0
                continue
            if v in gph[u]:
                e = gph[u][v]
                matrix[u][v] = e

    for k in nodes:
        for i in nodes:
            for j in nodes:
                if matrix[i][j] > matrix[i][k] + matrix[k][j]:
                    matrix[i][j] = matrix[i][k] + matrix[k][j]
    return matrix


def optimal_route(gph, visit, start=None, end=None, ignore_node=None, weight_attr=None):
    """Travelling Salesman
    ignore_node is an optional callable, if returns True then the node is ignored before branching
    Uses recursion and memoizes"""

    def shortest_path(cur, to_visit, path):
        """Returns the dist, path or None"""
        state = (cur, to_visit)
        if state in memo:
            return memo[state]

        if len(to_visit) == 0:
            return 0, path

        shortest = inf
        for n, d in adj_mtx[cur].items():
            if n not in to_visit:
                continue
            if ignore_node:
                if ignore_node(cur, to_visit, path):
                    continue
            if n == end and len(to_visit) > 1:
                continue

            n_path = path.copy()
            n_path.append(n)
            ntv = set(to_visit)
            ntv.remove(n)
            ntv = frozenset(ntv)
            sp = shortest_path(n, ntv, n_path)
            if sp is not None:
                sp_d, sp_path = sp
                if sp_d + d < shortest:
                    shortest = sp_d + d
                    best_path = sp_path

        if shortest == inf:
            memo[state] = None
            return None

        ans = (shortest, best_path)
        memo[state] = ans
        return ans

    # dictionary to remember best result for a given state
    memo = {}

    # get the adjacency matrix (shortest paths between every pair of relevant nodes)
    relevant = visit.copy()
    if start:
        relevant |= {start}
    if end:
        relevant |= {end}
        visit |= {end}
    adj_mtx = get_adjacency_matrix(gph, nodes=relevant, weight_attr=weight_attr)

    if start:
        # we know where to start
        return shortest_path(start, frozenset(visit), [])

    # where's the best place to start
    best_dst = inf
    best = None
    for n in visit:
        vst = visit.copy()
        vst.remove(n)
        dst, pth = shortest_path(n, frozenset(vst), [n])
        if dst < best_dst:
            best_dst = dst
            best = (dst, pth)
    return best


def reachable(gph, u):
    """Return a set of reachable nodes"""
    bfs = deque()
    bfs.append(u)
    seen = set()
    while bfs:
        u = bfs.popleft()
        if u in seen:
            continue
        seen.add(u)
        for v in gph[u]:
            bfs.append(v)
    return seen


def subgraph_nodes(gph) -> int:
    """Return a list of sets of subgraph nodes"""
    all_nodes = set(gph)
    subgraphs = []
    while all_nodes:
        a = list(all_nodes)[0]
        sg = reachable(gph, a)
        all_nodes.difference_update(sg)
        subgraphs.append(sg)
    return subgraphs


def remove_node(g, n):
    """Remove node n from graph g"""
    n_neighbours = list(g[n])
    for nn in n_neighbours:
        if n in g[nn]:
            del g[nn][n]
    del g[n]


def get_edge(g, u, v):
    """Get an edge for undirected graph"""
    if u in g:
        if v in g[u]:
            return g[u][v]
    if v in g:
        if u in g[v]:
            return g[v][u]
    return None


def add_edge(g, u, v, w=1):
    """Add a directed edge"""
    n = g.get(u, {})
    n[v] = w
    g[u] = n


def set_edge(g, u, v, w=1):
    """Set an edge in our undirected graph"""
    add_edge(g, u, v, w=w)
    add_edge(g, v, u, w=w)


def merge_nodes_keep_first(g, u, v):
    """Merge v into u accumulating edges of common neighbours"""
    for vn, w in g[v].items():
        if vn != u:
            if vn not in g[u]:
                set_edge(g, u, vn, w)
            else:
                nw = get_edge(g, u, vn)
                nw += w
                set_edge(g, u, vn, nw)
    remove_node(g, v)


def stoer_wagner(g):
    """Stoer-Wagner using a priority queue
    To return the minimum cut of edges that will divide the graph into 2.
    Keep merging nodes until left with 2, return the best cut and resulting partition
    Using a maximum binary heap we can reduce the time spent finding s,t
    """
    g = deepcopy(g)
    node_set = set(g)
    contractions = []  # contracted node pairs
    n = len(g)
    cut_value = inf

    for i in range(n - 1):
        # each iteration is a cut of the phase, where we will remove a node
        # via merging t into s

        any_start = list(g.keys())[0]  # get any element to start with
        A = {any_start}  # A as used in the original paper

        # create a maximum binary heap of all the nodes connected to
        # to the start using -ve weights this gives a maximum heap
        # on a minimum binary heap

        # so the top of heap is the node most connected to the start node
        h = BinaryHeap()
        for v, w in g[any_start].items():
            h.upsert(v, -w)

        # keep adding to A until we are at the last (t-node)
        for _ in range(n - i - 2):
            # get the node with the most connectivity to A
            # we just need to pop the heap
            u = h.pop()[0]
            A.add(u)

            # we now need to update the connectivity (the heap value)
            # of all the nodes connected to it not yet visited
            # their values now represent how well the node is connected to set A
            # so next time though this loop we get the next node to add to A

            # using the heap has saved re-evaluating the connectivity

            for v, w in g[u].items():
                if v not in A:
                    h.upsert(v, h.get(v, 0) - w)

        # we've now completed the minimum cut phase for the ith phase
        # the cut of the phase is A|t in that A is one side and t is the other
        # the top of the heap is t (as s has been popped and added to A)

        # we now have s,t as defined in the paper (the last 2 nodes in the cut phase)
        s = u
        t, w = h.min()
        w = -w  # flip it back to a +ve value

        # keep our best cut of a phase updated, i.e. our best phase
        if w < cut_value:
            cut_value = w
            best_phase = i

        # keep a record of the contractions (merging t into s)
        contractions.append((s, t))
        merge_nodes_keep_first(g, s, t)

    # create a graph of all the contractions up to the best phase (not inc)
    # this will be 2 separate subgraphs and we do not include the contraction
    # on the best phase since this is where the 2 subgraphs are joined.
    contractions_graph = {}
    for c in contractions[:best_phase]:
        set_edge(contractions_graph, c[0], c[1])

    # our focus is on the t-node of the best phase
    # since contractions occur on both sides of the cut
    # we want to only get the ones on the same side
    t = contractions[best_phase][1]

    # we might need to add the t-node in the "best" contraction
    # it should be there but dijkstra will definitely need a source
    # if it is not present then our partition will be the empty set
    # meaning no cut could found and seems meaningless
    # if t not in gc:
    #     gc[t] = {}

    # we use dijkstra to get all the connected nodes to the t-node
    # of the best cut, giving our final result
    node_partition_a = set(dijkstra(contractions_graph, t, None))
    node_partition_b = node_set - node_partition_a
    return cut_value, (node_partition_a, node_partition_b)


def which_edges_wagner(gph, sg1, sg2):
    to_cut = set()
    for u in sg1:
        for v in gph[u]:
            if v in sg2:
                to_cut.add((u, v))
    return to_cut


def tarjan(gph):
    """Return the strongly connected sub graphs"""

    def strong_connect(v):
        nonlocal idx
        low_link[v] = idx
        index_of[v] = idx
        idx += 1
        stk.append(v)
        on_stack.add(v)

        if v in gph:
            for w in gph[v]:
                if w not in index_of:
                    strong_connect(w)
                    low_link[v] = min(low_link[v], low_link[w])
                elif w in on_stack:
                    low_link[v] = min(low_link[v], index_of[w])

        if low_link[v] == index_of[v]:
            scc = []
            while True:
                w = stk.pop()
                scc.append(w)
                on_stack.discard(w)
                if w == v:
                    break
            sub_graphs.append(scc)

    idx = 0
    stk = deque()
    low_link = {}
    index_of = {}
    sub_graphs = []
    on_stack = set()
    for n in gph:
        if n in low_link:
            continue
        strong_connect(n)

    return sub_graphs


def minimal_spanning_tree(gph):
    """Applies Prim's algorithm to compute a minimum spanning tree on an undirected graph
    Returns a graph
    """
    mst = defaultdict(dict)
    h = BinaryHeap()
    parent = {}

    for v in gph:
        parent[v] = None
        h.upsert(v, inf)

    while h._dict:
        v, _ = h.pop()

        predecessor = parent[v]
        if predecessor is not None:
            weight = gph[predecessor][v]
            mst[predecessor][v] = weight

        for w in gph[v]:
            if h.get(w) is not None:
                new_key = gph[v][w]
                if new_key < h.get(w):
                    h.upsert(w, new_key)
                    parent[w] = v

    return mst


def kruskal_mst(gph):
    """Minimal spanning tree using Kruskal's algorithm
    This can also be used for maximum spanning tree if weights are negated
    and also works on graphs not strongly connected
    Edges are returned as dictionary
    """

    def find(parent, i):
        if parent[i] == i:
            return i
        return find(parent, parent[i])

    def union(parent, rank, x, y):
        x_root = find(parent, x)
        y_root = find(parent, y)

        if rank[x_root] < rank[y_root]:
            parent[x_root] = y_root
        elif rank[x_root] > rank[y_root]:
            parent[y_root] = x_root
        else:
            parent[y_root] = x_root
            rank[x_root] += 1

    result = {}
    i = 0
    e = 0
    edges = directed_edges(gph)
    edges = {(frozenset(e), w) for e, w in edges.items()}
    nodes = all_nodes(gph)
    V = len(nodes)

    edges = sorted(edges, key=lambda x: x[1])
    parent = [i for i in range(V)]
    rank = [0] * V

    while e < V - 1:
        (u, v), w = edges[i]
        i += 1
        x = find(parent, u)
        y = find(parent, v)

        if x != y:
            e += 1
            result[(u, v)] = w
            union(parent, rank, x, y)

    return result


def reverse_graph(gph):
    """Return the reverse of a directed graph"""
    rev_gph = defaultdict(dict)
    for u in gph:
        for v in gph[u]:
            rev_gph[v][u] = gph[u][v]
    return rev_gph


def directed_edges(gph):
    """Return a dict of edges keyed on a tuple (from,to) of a directed graph value is weight"""
    edges = {}
    for u in gph:
        for v, w in gph[u].items():
            edges[(u, v)] = w
    return edges


def edges_to_graph(edges, directed=True):
    """Return a graph given edges with weights"""
    gph = defaultdict(dict)
    for (u, v), w in edges.items():
        gph[u][v] = w
        if not directed:
            gph[v][u] = w
    return gph


def possible_roots(gph, check_all_nodes_reachable=True):
    """Find all possible roots of a directed graph"""
    scc_node_groups = tarjan(gph)
    edges = directed_edges(gph)
    scc_with_no_incoming_edges = set()
    for scc_nodes in scc_node_groups:
        incoming_edges = {
            v for (u, v), _ in edges.items() if u not in scc_nodes and v in scc_nodes
        }
        if incoming_edges:
            continue
        scc_with_no_incoming_edges.add(frozenset(scc_nodes))

    if len(scc_with_no_incoming_edges) != 1:
        return None

    # this is the only scc with no incoming from other groups
    # so it must be the root (all members can be roots by definition of scc)
    scc = scc_with_no_incoming_edges.pop()

    if check_all_nodes_reachable:
        reachable_nodes = reachable(gph, list(scc)[0])
        for scc_nodes in scc_node_groups:
            if scc_nodes == scc:
                continue
            if scc_nodes[0] in reachable_nodes:
                continue
            raise ValueError(f"Unreachable nodes {scc_nodes}")
    return scc


def find_a_circle(gph):
    """Return the first circle found as a set of edges, nodes"""
    sg_nodes = tarjan(gph)
    groups = [ns for ns in sg_nodes if len(ns) > 1]
    if not groups:
        return None, None

    group = groups[0]
    circle = set()
    nodes = set()
    src = group[0]
    group = set(group)
    cur = src
    prv = None
    group.remove(src)
    while True:
        nodes.add(cur)
        prv = cur
        neighbours = [x for x in gph[cur] if x in group]
        if len(neighbours) == 0:
            break
        cur = neighbours[0]
        group.remove(cur)
        circle.add((prv, cur))
    circle.add((cur, src))

    return circle, nodes


def edmond_mst(gph, root):
    """Return edges of a directed graph that form a minimal spanning tree
    ref: Wikipedia"""

    rev = reverse_graph(gph)
    E = directed_edges(gph)
    # remove any edge going into root
    for n in rev[root]:
        del E[(n, root)]

    P = {}
    v_src = {}
    # for every node
    for v, e in rev.items():
        if not e:
            continue
        if v == root:
            continue
        # edge into v with the lowest weight
        pi_v, pi_v_w = sorted([(u, w) for u, w in e.items()], key=lambda x: x[1])[0]
        P[(pi_v, v)] = pi_v_w
        v_src[v] = pi_v

    tg = edges_to_graph(P)
    edge_circle, node_circle = find_a_circle(tg)

    if edge_circle is None:
        return P

    vc_cnt = 0
    while True:
        vc = f"_tmp_vc_{vc_cnt}"
        if vc not in gph:
            break
        vc_cnt += 1

    E2 = {}
    corresponding_edges = {}
    for (u, v), w in E.items():
        if u not in node_circle and v in node_circle:

            nw = w - P[(v_src[v], v)]

            if (u, vc) in E2:
                if w < E2[(u, vc)]:
                    E2[(u, vc)] = nw
                    corresponding_edges[(u, vc)] = (u, v)
            else:
                E2[(u, vc)] = nw
                corresponding_edges[(u, vc)] = (u, v)
            continue

        if u in node_circle and v not in node_circle:
            if (vc, v) in E2:
                if w < E2[(vc, v)]:
                    E2[(vc, v)] = w
                    corresponding_edges[(vc, v)] = (u, v)
            else:
                E2[(vc, v)] = w
                corresponding_edges[(vc, v)] = (u, v)
            continue

        if u not in node_circle and v not in node_circle:
            E2[(u, v)] = w
            corresponding_edges[(u, v)] = (u, v)
            continue

    ng = edges_to_graph(E2)
    A2 = edmond_mst(ng, root=root)
    into_vc = [n for (n, v) in A2 if v == vc]
    assert len(into_vc) == 1
    u = into_vc[0]

    (u, v) = corresponding_edges[(u, vc)]
    edge_circle.remove((v_src[v], v))

    A = {}
    for e, w in A2.items():
        ce = corresponding_edges[e]
        A[ce] = E[ce]
    for e in edge_circle:
        A[e] = E[e]

    return A


def minimal_spanning_tree_directed(gph, as_edges=False):
    """Return the minimal spanning arborescence using Edmonds algorithm
    as a graph"""
    roots = possible_roots(gph)
    if not roots:
        raise ValueError("Directed graph has no root that will span all nodes")
    best_mst = None
    best_mst_value = inf
    for v in roots:
        mst = edmond_mst(gph, v)
        print(v)
        print(mst)
        value = sum(mst.values())
        if value < best_mst_value:
            best_mst_value = value
            best_mst = mst
    if not as_edges:
        best_mst = edges_to_graph(best_mst)
    return best_mst


test_data = [
    ("A", "B", 1),
    ("A", "C", 2),
    ("A", "D", 3),
    ("B", "A", 7),
    ("B", "C", 4),
    ("B", "D", 5),
    ("C", "A", 8),
    ("C", "B", 10),
    ("C", "D", 6),
    ("D", "A", 9),
    ("D", "B", 11),
    ("D", "C", 12),
]

# import networkx as nx

# dg = nx.DiGraph()
# gph = defaultdict(dict)
# for u, v, w in test_data:
#     gph[u][v] = w
#     # dg.add_edge(u, v, w=w)

# print("min")
# a = nx.minimum_spanning_arborescence(dg, "w")
# for u, v, w in a.edges(data=True):
#     print(u, v, w)

# print("max")
# a = nx.maximum_spanning_arborescence(dg, "w")
# for u, v, w in a.edges(data=True):
#     print(u, v, w)

# a = edmond_mst(gph, root="A")
# print(a)

# a = minimal_spanning_tree_directed(gph, as_edges=True)
# print(a)

# pr = possible_roots(gph)
# print(pr)

# dt = [(0, 1, 10), (0, 2, 6), (0, 3, 5), (1, 3, 15), (2, 3, 4)]

# gph = defaultdict(dict)
# for u, v, w in dt:
#     add_edge(gph, u, v, w)
#     add_edge(gph, v, u, w)

# m = minimal_spanning_tree(gph)
# print(m)

#########################################################################
# Tests using
# https://algorithms.discrete.ma.tum.de/
#########################################################################


def make_test_graph(gd: str, directed=False, use_alpha=False):
    gph = defaultdict(dict)
    for line in gd.splitlines():
        if not line:
            continue
        arr = tok(line.strip())
        e = tuple(int(x) for x in arr[1:])
        u = e[0]
        v = e[1]
        if use_alpha:
            u = chr(ord("a") + u)
            v = chr(ord("a") + v)
        gph[u][v] = e[3]
        if directed:
            continue
        gph[v][u] = e[3]
    return gph


def make_test_matrix(md: str):
    nodes = []
    for line in md.splitlines():
        if not line:
            continue
        arr = tok(line, delim="\t")
        nodes.append(arr[0])

    mtx = defaultdict(dict)
    for line in md.splitlines():
        if not line:
            continue
        arr = tok(line, delim="\t")
        u = arr[0]
        for i, x in enumerate(arr[1:]):
            v = nodes[i]
            w = inf
            if x.isnumeric():
                w = int(x)
            mtx[u][v] = w
    return mtx


def test_prim():
    g_data = """
e 2 4 0 33
e 3 5 1 2
e 3 4 2 20
e 4 5 3 1
e 2 3 4 20
e 1 4 5 10
e 1 3 6 50
e 0 2 7 20
e 0 1 9 10
"""
    gph = make_test_graph(g_data)
    mst = minimal_spanning_tree(gph)
    kru = kruskal_mst(gph)
    edges = directed_edges(mst)
    assert sum(w for _, w in edges.items()) == 43
    assert sum(kru.values()) == 43


def test_floyd():
    g_data = """
e 0 1 0 4
e 1 2 1 9
e 0 6 2 7
e 0 7 3 4
e 1 7 4 1
e 7 2 5 3
e 1 6 6 8
e 6 1 7 4
e 6 5 8 7
e 1 5 9 6
e 5 4 10 6
e 4 5 11 5
e 4 3 12 6
e 2 4 13 10
e 4 2 14 8
"""

    m_data = """
a	0	4	7	22	16	10	7	4
b	∞	0	4	18	12	6	8	1
c	∞	∞	0	16	10	15	∞	∞
d	∞	∞	∞	0	∞	∞	∞	∞
e	∞	∞	8	6	0	5	∞	∞
f	∞	∞	14	12	6	0	∞	∞
g	∞	4	8	19	13	7	0	5
h	∞	∞	3	19	13	18	∞	0
"""

    gph = make_test_graph(g_data, use_alpha=True, directed=True)
    mtx = make_test_matrix(m_data)
    f = floyd_warshall(gph)
    am = get_adjacency_matrix(gph, include_unreachable=True, include_diagonal=True)
    for u, e in mtx.items():
        for v, w in e.items():
            assert f[u][v] == w
            assert am[u][v] == w


def test_bellman_ford():
    g_data = """
e 2 4 0 33
e 3 5 1 -2
e 3 4 2 -20
e 4 5 3 1
e 2 3 4 20
e 1 4 5 10
e 1 3 6 50
e 0 2 7 20
e 0 1 8 10
"""
    gph = make_test_graph(g_data, directed=True)
    bf = bellman_ford(gph, 5)
    assert all(w == inf for v, w in bf.items() if v != 5)
    bf = bellman_ford(gph, 0)
    assert bf == {0: 0, 1: 10, 2: 20, 3: 40, 4: 20, 5: 21}

    g_data = """
e 0 1 0 10
e 1 2 1 1
e 2 4 2 3
e 4 3 3 -10
e 3 1 4 4
e 4 5 5 22
"""
    gph = make_test_graph(g_data, directed=True)
    try:
        bf = bellman_ford(gph, 0)
        raise RuntimeError("Should fail")
    except ValueError:
        pass


# test_bellman_ford()
# test_floyd()
# test_prim()
