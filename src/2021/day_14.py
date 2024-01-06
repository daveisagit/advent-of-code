"""Advent of code 2021
--- Day 14: Extended Polymerization ---
"""

from collections import Counter, defaultdict
from itertools import pairwise
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    template = raw_data[0]
    rules = {}
    for line in raw_data[2:]:
        arr = tok(line, delim="->")
        rules[arr[0]] = arr[1]
    return template, rules


def iterate(polymer: list, rules):
    """As per instructions"""
    pairs = pairwise(polymer)
    nxt = []
    for a, b in pairs:
        k = a + b
        if k in rules:
            nxt.append(a)
            nxt.append(rules[k])
        else:
            nxt.append(a)
            print("no rule", a, b)

    nxt.append(b)
    return nxt


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    template, rules = data
    polymer = list(template)
    for _ in range(10):
        polymer = iterate(polymer, rules)
    cnt = Counter(polymer)
    mc = cnt.most_common()
    return mc[0][1] - mc[-1][1]


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B

    Recording counts against a pair means we do need to retain the
    previous state

    i.e. CB -> CH & HB

    This will double count the inserted element
    but means we can forget about the spawning pair

    i.e. take off 1 for the CB count and add 1 to CH and HB

    We just need to account for the ends by adding 1 to the count
    of the final element count for those 2 elements
    """

    def new_pairs(pair):
        c = rules[pair]
        return pair[0] + c, c + pair[1]

    template, rules = data

    # initialise the pair count as per the template
    pair_count = {p: 0 for p in rules}
    pairs = [a + b for a, b in pairwise(template)]
    for p in pairs:
        pair_count[p] += 1

    for _ in range(40):
        # how many new pairs are being added
        new_pair_count = defaultdict(int)
        for p, cnt in pair_count.items():
            a, b = new_pairs(p)
            new_pair_count[a] += cnt
            new_pair_count[b] += cnt

        # remove the current count and add the new
        for p, cnt in pair_count.items():
            pair_count[p] += new_pair_count[p] - cnt

    # split each pair for counting
    elements = defaultdict(int)
    for p, cnt in pair_count.items():
        elements[p[0]] += cnt
        elements[p[1]] += cnt

    # half the count
    elements = {e: cnt // 2 for e, cnt in elements.items()}

    # add 1 for the ends
    elements[template[0]] += 1
    elements[template[-1]] += 1

    e_vals = sorted(elements.values())

    return e_vals[-1] - e_vals[0]


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)


MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
