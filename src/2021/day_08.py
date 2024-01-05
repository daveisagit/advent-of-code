"""Advent of code 2021
--- Day 8: Seven Segment Search ---
"""

from collections import defaultdict
from itertools import permutations
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        arr = tok(line, delim="|")
        signal_patterns = tok(arr[0])
        digits = tok(arr[1])
        data.append((signal_patterns, digits))
    return data


wires = "abcdefg"

digit_to_segments = {
    0: "abcefg",
    1: "cf",
    2: "acdeg",
    3: "acdfg",
    4: "bcdf",
    5: "abdfg",
    6: "abdefg",
    7: "acf",
    8: "abcdefg",
    9: "abcdfg",
}

segments_to_digits = {s: d for d, s in digit_to_segments.items()}

all_lengths = defaultdict(list)
for d, s in digit_to_segments.items():
    all_lengths[len(s)].append(d)


unique_lengths = {seg_len for seg_len, lst in all_lengths.items() if len(lst) == 1}


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    all_unique_digits = [
        digit for _, digits in data for digit in digits if len(digit) in unique_lengths
    ]
    return len(all_unique_digits)


def resolve_signal_map_neat(signals) -> dict:
    """Given a set of signals output a mapping to the defaults"""

    def map_valid(m):
        """Return True if the map is valid"""
        for signal in signals:
            if len(signal) in unique_lengths:
                continue
            act_signal = "".join(sorted([m[c] for c in signal]))
            if act_signal not in digit_to_segments.values():
                return False
        return True

    signal_1 = set([signal for signal in signals if len(signal) == 2][0])
    signal_7 = set([signal for signal in signals if len(signal) == 3][0])
    signal_4 = set([signal for signal in signals if len(signal) == 4][0])

    restrictions = []
    restrictions.append(signal_7 - signal_1)  # a
    restrictions.append(signal_4 - signal_1)  # b
    restrictions.append(signal_1)  # c
    restrictions.append(signal_4 - signal_1)  # d
    restrictions.append(None)  # e
    restrictions.append(signal_1)  # f
    restrictions.append(None)  # g

    for arrangement in permutations(list(wires)):
        ignore = False
        for pos, restriction in enumerate(restrictions):
            if restriction and arrangement[pos] not in restriction:
                ignore = True
                break
        if ignore:
            continue

        m = {c: wires[i] for i, c in enumerate(arrangement)}
        if map_valid(m):
            return m


def resolve_signal_map_fast(signals) -> dict:
    """Given a set of signals output a mapping to the defaults
    This is the original first attempt but I did not like the nested for loops
    Turns out it is quicker that the more neater permutation method"""
    options = {w: set(wires) for w in wires}

    def map_valid(m):
        """Return True if the map is valid"""
        for signal in signals:
            if len(signal) in unique_lengths:
                continue
            act_signal = "".join(sorted([m[c] for c in signal]))
            if act_signal not in digit_to_segments.values():
                return False
        return True

    signal_1 = set([signal for signal in signals if len(signal) == 2][0])
    signal_7 = set([signal for signal in signals if len(signal) == 3][0])
    signal_4 = set([signal for signal in signals if len(signal) == 4][0])

    options["a"] = signal_7 - signal_1
    options["c"] = signal_1
    options["f"] = signal_1
    options["b"] = signal_4 - signal_1
    options["d"] = signal_4 - signal_1

    for a_map in options["a"]:
        for b_map in options["b"]:
            for c_map in options["c"]:
                for d_map in options["d"]:
                    for e_map in options["e"]:
                        for f_map in options["f"]:
                            for g_map in options["g"]:
                                m = {
                                    a_map: "a",
                                    b_map: "b",
                                    c_map: "c",
                                    d_map: "d",
                                    e_map: "e",
                                    f_map: "f",
                                    g_map: "g",
                                }
                                if len(m) != 7:
                                    continue
                                if map_valid(m):
                                    return m


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    values = []
    for signals, digits in data:
        m = resolve_signal_map_neat(signals)
        pl = 1000
        v = 0
        for en in digits:
            de = "".join(sorted([m[c] for c in en]))
            digit = segments_to_digits[de]
            v += digit * pl
            pl = pl // 10
        values.append(v)

    return sum(values)


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
