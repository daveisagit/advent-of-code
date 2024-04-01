"""Graphing tools"""

from collections import deque
from heapq import heappop, heappush
from itertools import count
from math import inf


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


def simplify(gph, protected_nodes=None):
    """Remove nodes and merge edges for nodes with 2 edges
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
        gph[u][v] = e_sum
        gph[v][u] = e_sum
        del gph[n]
        candidates = {u for u, oe in gph.items() if len(oe) == 2}
        candidates.difference_update(protected_nodes)


def get_adjacency_matrix(gph, nodes=None, weight_attr=None):
    """Returns the adjacency matrix (as dict)"""
    matrix = {}
    if nodes is None:
        nodes = set(gph)
    for u in nodes:
        distances, _ = dijkstra_paths(gph, u, weight_attr=weight_attr)
        matrix[u] = {}
        for v, d in distances.items():
            if u == v:
                continue
            matrix[u][v] = d
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

        ans = shortest
        if shortest == inf:
            ans = None
            memo[state] = None
            return None

        ans = (ans, best_path)
        memo[state] = ans
        return ans

    # dictionary to remember best result for a given state
    memo = {}

    # get the adjacency matrix (shortest paths between every pair of relevant nodes)
    relevant = visit
    if start:
        relevant |= {start}
    if end:
        relevant |= {end}
        visit |= {end}
    adj_mtx = get_adjacency_matrix(gph, nodes=relevant, weight_attr=weight_attr)

    if start:
        # we know where to start
        return shortest_path(start, frozenset(visit), [])
    else:
        # where's the best place to start
        best_dst = inf
        best = None
        for n in visit:
            vst = visit.copy()
            vst.remove(n)
            dst, pth = shortest_path(n, frozenset(vst), [n])
            if dst < best_dst:
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
