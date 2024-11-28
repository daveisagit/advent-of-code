"""Advent of code 2020
--- Day 16: Ticket Translation ---
"""

from collections import defaultdict
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok
from common.logic import exact_cover, mapping_options


def parse_data(raw_data):
    """Parse the input"""
    rules = []
    for i, line in enumerate(raw_data):
        if not line:
            break
        arr = tok(line, ":")
        rule_name = arr[0]
        arr = tok(arr[1], "or")
        rule = []
        for r in arr:
            ri = [int(x) for x in tok(r, "-")]
            rule.append(ri)
        rules.append(rule)

    yt = [int(x) for x in raw_data[i + 2].split(",")]

    nb = []
    for i, line in enumerate(raw_data[i + 5 :]):
        nb.append([int(x) for x in line.split(",")])

    return rules, yt, nb


def invalid_values(ticket, rules):
    """Return a set of invalid values on this ticket"""
    inv_val = set()
    for fv in ticket:
        complies = False
        for r in rules:
            if complies:
                break
            for opt in r:
                if opt[0] <= fv <= opt[1]:
                    complies = True
                    break
        if not complies:
            inv_val.add(fv)
    return inv_val


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    rules, _, nearby = data
    sr = 0
    for ticket in nearby:
        vals = invalid_values(ticket, rules)
        if vals:
            sr += sum(vals)
    return sr


def dump_matrix(rf):
    """Visual"""
    print()
    for r in rf:
        line = ["X" if v else " " for v in r]
        print(" ".join(line))


def apply_inference(rf):
    """Look for and apply inferences"""
    change_made = False
    sz = len(rf)
    inferences = []
    for ri, fields in enumerate(rf):
        possible_fields = [fi for fi, pos in enumerate(fields) if pos]
        if len(possible_fields) == 1:
            inferences.append((ri, possible_fields[0]))

    for r, c in inferences:
        for i in range(sz):
            if i == r:
                continue
            if rf[i][c] is True:
                change_made = True
            rf[i][c] = False

    return change_made


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    rules, ours, nearby = data
    valid_tickets = [ticket for ticket in nearby if not invalid_values(ticket, rules)]

    # rule / field matrix
    rf = []
    c = len(rules)
    for _ in range(c):
        fp = list(False for _ in range(c))
        rf.append(fp)

    # initialize the matrix based on ticket data
    for ri, rule in enumerate(rules):
        for fi in range(c):
            valid_on_all = True
            for ticket in valid_tickets:
                fv = ticket[fi]
                valid_ticket = False
                for opt in rule:
                    if opt[0] <= fv <= opt[1]:
                        valid_ticket = True
                        break
                if not valid_ticket:
                    valid_on_all = False
                    break
            rf[ri][fi] = valid_on_all

    # apply inferences
    changes_made = True
    while changes_made:
        changes_made = apply_inference(rf)

    # map rule to field
    rule_to_field = [
        ci for ri, fields in enumerate(rf) for ci, v in enumerate(fields) if v
    ]

    which_rules = 3
    if len(rules) == 20:
        which_rules = 6
    ans = 1
    for rule in range(which_rules):
        fi = rule_to_field[rule]
        v = ours[fi]
        ans *= v

    return ans


@aoc_part
def solve_part_c(data) -> int:
    """Solve part B"""
    rules, ours, nearby = data
    valid_tickets = [ticket for ticket in nearby if not invalid_values(ticket, rules)]

    maps = defaultdict(set)

    # Build a dict of sets - mapping options for rule to field
    # if a field is valid on all tickets then its viable
    for ri, rule in enumerate(rules):
        for fi in range(len(rules)):
            valid_on_all = True
            for ticket in valid_tickets:
                fv = ticket[fi]
                valid_ticket = False
                for opt in rule:
                    if opt[0] <= fv <= opt[1]:
                        valid_ticket = True
                        break
                if not valid_ticket:
                    valid_on_all = False
                    break
            if valid_on_all:
                maps[ri].add(fi)

    rule_to_field = list(mapping_options(maps))
    assert len(rule_to_field) == 1
    rule_to_field = rule_to_field[0]

    which_rules = 3
    if len(rules) == 20:
        which_rules = 6
    ans = 1
    for rule in range(which_rules):
        fi = rule_to_field[rule]
        v = ours[fi]
        ans *= v

    return ans


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)


MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)


solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)

solve_part_c(EX_DATA)
solve_part_c(MY_DATA)
