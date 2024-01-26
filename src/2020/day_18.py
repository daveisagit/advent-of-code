"""Advent of code 2020
--- Day n: ---
"""

from collections import deque
from common.aoc import file_to_list, aoc_part, get_filename


def parse_data(raw_data):
    """Parse the input"""
    data = []
    for line in raw_data:
        expr = [c for c in line if c != " "]
        expr = [int(c) if c.isdigit() else c for c in expr]
        data.append(expr)
    return data


def my_eval(data: list):
    """My eval"""
    val = 0
    last_op = "+"
    while data:
        t = data.pop(0)

        if isinstance(t, int):
            if last_op == "+":
                val += t
            else:
                val *= t
            continue

        if t in "+*":
            last_op = t
            continue

        if t == "(":
            res = my_eval(data)
            data.insert(0, res)
            continue

        if t == ")":
            return val

    return val


@aoc_part
def solve_part_a(data) -> int:
    """Solve part A"""
    s = 0
    for expr in data:
        s += my_eval(expr.copy())
    return s


def eval_using_shunt(data: list):
    """Use the shunting algorithm to create a RPN for stack calculation"""
    out_que = deque()
    opr_stk = deque()

    for t in data:
        if isinstance(t, int):
            out_que.append(t)
            continue

        if t == "(":
            opr_stk.append(t)
            continue

        if t == ")":
            while opr_stk:
                top = opr_stk.pop()
                if top == "(":
                    break
                out_que.append(top)

        if t in "+*":
            while opr_stk:
                top = opr_stk[-1]
                # if the top of the stack is ( then add on top
                if top == "(":
                    break
                # + has higher precedence over * so we simply
                # add to opr stack
                if top != t and top == "*" and t == "+":
                    break
                # if the precedence is the same or lower than what
                # is on the stack then move to the out_que
                top = opr_stk.pop()
                out_que.append(top)
            opr_stk.append(t)
            continue

    # move the remainder of the opr stack to the output queue
    while opr_stk:
        out_que.append(opr_stk.pop())

    # process the output queue in RPN
    # put numbers on the stack, operators take off
    # the top 2 items and put the result back on
    stk = deque()
    while out_que:
        t = out_que.popleft()
        if isinstance(t, int):
            stk.append(t)
            continue
        a = stk.pop()
        b = stk.pop()
        if t == "*":
            r = a * b
        else:
            r = a + b
        stk.append(r)

    return stk.pop()


@aoc_part
def solve_part_b(data) -> int:
    """Solve part B"""
    s = 0
    for expr in data:
        s += eval_using_shunt(expr)
    return s


EX_RAW_DATA = file_to_list(get_filename(__file__, "ex"))
EX_DATA = parse_data(EX_RAW_DATA)

MY_RAW_DATA = file_to_list(get_filename(__file__, "my"))
MY_DATA = parse_data(MY_RAW_DATA)

solve_part_a(EX_DATA)
solve_part_a(MY_DATA)

solve_part_b(EX_DATA)
solve_part_b(MY_DATA)
