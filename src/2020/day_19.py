"""Advent of code 2020
--- Day 19: Monster Messages ---
"""

from itertools import product
from common.aoc import file_to_list, aoc_part, get_filename
from common.general import tok


def parse_data(raw_data):
    """Parse the input"""
    rules = {}
    for i, line in enumerate(raw_data):
        if not line:
            break
        arr = tok(line, ":")
        rule_id = int(arr[0])
        rule_val = arr[1]
        if rule_val.startswith('"'):
            rules[rule_id] = rule_val[1]
            continue

        set_of_seq = []
        seqs = tok(rule_val, "|")
        for seq in seqs:
            sub_rules = tok(seq)
            sub_rules = [int(r) for r in sub_rules]
            set_of_seq.append(tuple(sub_rules))
        rules[rule_id] = tuple(set_of_seq)

    messages = []
    for line in raw_data[i + 1 :]:
        messages.append(line)

    return rules, messages


def all_valid_messages(rules, root):
    """Generate all possible valid messages for a given rule"""

    # memoize the list of possible messages for each rule
    # this however has little affect for part A
    memo = {}

    def possible_messages_for_rule(rule_id):
        if rule_id in memo:
            return memo[rule_id]

        rule = rules[rule_id]
        if isinstance(rule, str):
            memo[rule_id] = [rule]
            return [rule]

        # messages is a list of all the possible messages for this rule
        messages = []
        for seq in rule:
            # an item in possibles is a list of possible messages
            # for the sub-rule in the given sequence
            possibles = []
            for sub_rule_id in seq:
                possibles.append(possible_messages_for_rule(sub_rule_id))
            # we extend messages for each OR'd sequence
            # a sequence will give rise to a cartesian product of lists in possibles
            messages.extend(list(product(*possibles)))

        messages = ["".join(msg) for msg in messages]
        memo[rule_id] = messages
        return messages

    possible_messages_for_rule(root)

    return memo


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    rules, messages = data
    memo = all_valid_messages(rules, 0)
    valid_messages = [msg for msg in messages if msg in memo[0]]
    return len(valid_messages)


def matches_rule_0(msg, memo):
    """Does the message match the new rules"""
    og_msg = msg

    # rule 0 = 8 11 so we remove an equal number
    # of 42s and 31s from the head and tail.
    while msg:
        match = False
        for ml in memo[42]:
            if match:
                break
            if msg.startswith(ml):
                for mr in memo[31]:
                    if msg.endswith(mr):
                        msg = msg[len(ml) : -len(mr)]
                        match = True
                        break

        if not match:
            break

    # if we removed all or nothing then it fails
    if not msg or og_msg == msg:
        return False

    # all that remains is a repeat of 42
    while msg:
        match = False
        for m in memo[42]:
            if msg.startswith(m):
                msg = msg[len(m) :]
                match = True
                break
        if not match:
            break

    return not msg


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    rules, messages = data
    memo = all_valid_messages(rules, 0)
    del memo[0]
    del memo[8]
    del memo[11]

    cnt = 0
    for msg in messages:
        if matches_rule_0(msg, memo):
            cnt += 1

    return cnt


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
