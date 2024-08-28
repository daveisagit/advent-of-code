"""Advent of code 2023
--- Day 20: Pulse Propagation ---
"""

from collections import deque
from math import lcm
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    modules = {}
    for line in raw_data:
        if line.startswith("broadcaster"):
            arr = tok(line, "->")
            broadcaster = tuple(tok(arr[1], ","))
            continue

        arr = tok(line, "->")
        mod_typ = arr[0][0]
        mod_id = arr[0][1:]
        mod_send = tuple(tok(arr[1], ","))

        modules[mod_id] = mod_typ, mod_send

    return broadcaster, modules


def initialise(modules):
    """Return the flip flops and conjunctions in their initial state"""
    flip_flops = {
        mod_id: False for mod_id, (mod_typ, _) in modules.items() if mod_typ == "%"
    }
    conjunctions = {
        mod_id: {
            m_id: False
            for m_id, (_, m_send_to) in modules.items()
            if mod_id in m_send_to
        }
        for mod_id, (mod_typ, _) in modules.items()
        if mod_typ == "&"
    }
    return flip_flops, conjunctions


def press_button(broadcaster, modules, flip_flops, conjunctions, pre_rx=None):
    """Put pulses onto a queue so they are handled in the order they are sent out.
    Return the counts of low/high and a set of modules that sent high to pre_rx"""

    pre_rx_received_high_from = set()  # for part B
    low_count = 1  # allow 1 for the initial button press
    high_count = 0

    q = deque()

    for m in broadcaster:
        q.append((None, m, False))

    while q:
        src, trg, pulse = q.popleft()

        if pulse:
            high_count += 1
            if trg == pre_rx:
                pre_rx_received_high_from.add(src)
        else:
            low_count += 1

        if trg in modules:
            mod_typ, mod_send = modules[trg]
        else:
            # rx ?
            continue

        if mod_typ == "%":
            if not pulse:
                flip_flops[trg] = not flip_flops[trg]
                for next_m in mod_send:
                    q.append((trg, next_m, flip_flops[trg]))

        else:
            conjunctions[trg][src] = pulse
            send = not all(c for c in conjunctions[trg].values())
            for next_m in mod_send:
                q.append((trg, next_m, send))

    return low_count, high_count, pre_rx_received_high_from


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    broadcaster, modules = data
    flip_flops, conjunctions = initialise(modules)

    low_count = 0
    high_count = 0

    for _ in range(1000):
        lc, hc, _ = press_button(broadcaster, modules, flip_flops, conjunctions)
        low_count += lc
        high_count += hc

    return low_count * high_count


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B
    low -> rx
    rx only receives from pre_rx,
    pre_rx receives from 4 key conjunction modules
    we need to know when all 4 are high
    find the congruence classes for when they go high
    """
    broadcaster, modules = data
    flip_flops, conjunctions = initialise(modules)
    pre_rx = [m for m, (_, st) in modules.items() if "rx" in st][0]
    key_modules = set(conjunctions[pre_rx].keys())
    occurrences = {km: [] for km in key_modules}
    cnt = 0
    while any(len(x) < 2 for x in occurrences.values()):
        _, _, pre_rx_received_high_from = press_button(
            broadcaster, modules, flip_flops, conjunctions, pre_rx
        )
        cnt += 1
        if pre_rx_received_high_from:
            for km in pre_rx_received_high_from:
                occurrences[km].append(cnt)

    # turns out they all repeat from zero so we only need the LCM
    congruences = [occurs[1] - occurs[0] for _, occurs in occurrences.items()]
    return lcm(*congruences)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(MY_DATA)
