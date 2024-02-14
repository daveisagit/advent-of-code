"""Graphing tools"""

from heapq import heappop, heappush
from itertools import count


def dijkstra(gph, source, target):
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
        for u, cost in gph[v].items():
            vu_dist = dist[v] + cost

            if u not in seen or vu_dist < seen[u]:
                seen[u] = vu_dist
                push(fringe, (vu_dist, next(c), u))

    if target:
        return dist[target]
    return dist


def simplify(gph):
    """Remove nodes and merge edges for nodes with 2 edges"""
    candidates = [u for u, oe in gph.items() if len(oe) == 2]
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
        candidates = [u for u, oe in gph.items() if len(oe) == 2]
