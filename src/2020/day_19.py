"""Advent of code 2020
--- Day 19: Monster Messages ---
"""

from itertools import product
import queue
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


def match_to_rules(rules, message, memo):
    """Does the message match the rules"""

    valid = False

    def check(msg, rule_id):
        nonlocal valid

        if isinstance(rule_id, str):
            return msg

        rule = rules[rule_id]
        if rule_id in memo:
            if msg in memo[rule_id]:
                return ""
            for match in memo[rule_id]:
                if msg.startswith(match):
                    return msg[len(match) :]
            return msg

        for seq in rule:
            failed = False
            msg2 = msg
            for sub_rule_id in seq:
                if not msg2:
                    failed = True
                    break
                msg2 = check(msg2, sub_rule_id)
            if msg2 == "" and not failed:
                valid = True
                return ""

    check(message, 0)
    return valid


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    rules, messages = data
    memo = all_valid_messages(rules, 0)
    del memo[0]
    del memo[8]
    del memo[11]
    # for rule_id, vml in memo.items():
    #     print(rule_id, vml)

    rules[8] = ((42,), (42, 8))
    rules[11] = (
        (
            42,
            31,
        ),
        (42, 11, 31),
    )

    for msg in messages:
        if match_to_rules(rules, msg, memo):
            print(msg)

    return 0


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

# solve_part_a(EX_DATA)
# solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
# solve_part_b(MY_DATA)
