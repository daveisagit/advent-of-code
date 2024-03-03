"""Advent of code 2018
--- Day 7: The Sum of Its Parts ---
"""

from collections import defaultdict
from copy import deepcopy
from common.aoc import file_to_list, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    next_dependents = defaultdict(dict)
    prev_prerequisites = defaultdict(dict)
    for line in raw_data:
        a = line[5]
        b = line[36]
        next_dependents[a][b] = 1
        prev_prerequisites[b][a] = 1
    return next_dependents, prev_prerequisites


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    data = deepcopy(data)
    next_dependents, prev_prerequisites = data
    all_nodes = set(next_dependents) | set(prev_prerequisites)
    start_nodes = all_nodes - set(prev_prerequisites)
    end_nodes = all_nodes - set(next_dependents)
    print(f"Start: {start_nodes}")
    print(f"End  : {end_nodes}")

    next_up = list(start_nodes)
    final = []
    while next_up:
        next_up = sorted(next_up)
        n = next_up.pop(0)
        final.append(n)
        fd = set(next_dependents[n])
        for m in fd:
            del next_dependents[n][m]
            del prev_prerequisites[m][n]
            if len(prev_prerequisites[m]) == 0:
                next_up.append(m)

    return "".join(final)


@aoc_part
def solve_part_b(data, num_workers=2, base_duration=0) -> int:
    """Solve part B"""

    def node_duration(n):
        return ord(n) - 64 + base_duration

    # data structures

    # next_dependents:     nodes dependent on me
    # prev_prerequisites:  nodes that must complete before I can start
    # end_times:           point in time when the node is complete
    # worker_ready_at:     array of workers and the time at which they are available
    # ok_to_go:            nodes that are ready to go and their earliest start time

    # While not done
    #   Find the unfinished nodes that can start (and their earliest start time) = ok_to_go
    #   Which of those are considered given our most ready worker
    #   Exists:     use first (alpha sort)
    #   Does not:   Find the most ready nodes (earliest possible start) and pick 1st by alpha
    #   End Time = start +duration, update end_times, worker_ready_at

    next_dependents, prev_prerequisites = data
    all_nodes = set(next_dependents) | set(prev_prerequisites)

    end_times = {n: 0 for n in all_nodes}
    worker_ready_at = [0] * num_workers
    while min(end_times.values()) == 0:
        unfinished = {n for n, t in end_times.items() if t == 0}
        ok_to_go = {}
        for u in unfinished:
            ready = True
            start_time = 0
            for v in prev_prerequisites[u]:
                if end_times[v] == 0:
                    ready = False
                    break
                if end_times[v] > start_time:
                    start_time = end_times[v]
            if ready:
                ok_to_go[u] = start_time

        worker_ready_at = sorted(worker_ready_at)
        start_time = worker_ready_at[0]

        ready_nodes = [n for n, st in ok_to_go.items() if st <= start_time]
        if ready_nodes:
            # worker waiting, who's ready?
            ready_nodes = sorted(ready_nodes)
        else:
            # workers not yet ready
            start_time = min(ok_to_go.values())
            ready_nodes = [n for n, st in ok_to_go.items() if st <= start_time]
            ready_nodes = sorted(ready_nodes)

        n = ready_nodes[0]
        st = max(ok_to_go[n], worker_ready_at[0])
        et = st + node_duration(n)
        end_times[n] = et
        worker_ready_at[0] = et

    return max(end_times.values())


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA, num_workers=5, base_duration=60)
