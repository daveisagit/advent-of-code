"""Parsing code"""

"""
Shunting Yard Algorithm to convert infix to postfix

1.  While there are tokens to be read:
2.        Read a token
3.        If it's a number add it to queue
4.        If it's an operator
5.               While there's an operator on the top of the stack with greater precedence:
6.                       Pop operators from the stack onto the output queue
7.               Push the current operator onto the stack
8.        If it's a left bracket push it onto the stack
9.        If it's a right bracket 
10.            While there's not a left bracket at the top of the stack:
11.                     Pop operators from the stack onto the output queue.
12.             Pop the left bracket from the stack and discard it
13. While there are operators on the stack, pop them to the queue

"""


from collections import deque


def get_precedence(op):
    precedences = {
        "+": 1,
        "-": 1,
        "*": 2,
        "/": 2,
        "//": 2,
        "%": 2,
        "^": 3,
    }
    return precedences.get(op, 0)


def infix_to_postfix(expr_list, precedence_callable=get_precedence):
    """Return a postfix stack (BNF) given an infix (expression)"""
    output = deque()
    stack = deque()

    for token in expr_list:
        if isinstance(token, int):
            output.append(token)
        elif token == "(":
            stack.append(token)
        elif token == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            stack.pop()  # Pop the left parenthesis
        else:
            while stack and precedence_callable(stack[-1]) >= precedence_callable(
                token
            ):
                output.append(stack.pop())
            stack.append(token)

    while stack:
        output.append(stack.pop())

    return output


def eval_postfix(expr: deque):
    """Return the evaluation of a postfix expression stack"""
    stk = []
    while expr:
        t = expr.popleft()
        if isinstance(t, int):
            stk.append(t)
            continue
        a = stk.pop()
        b = stk.pop()
        if t == "*":
            r = a * b
        elif t == "+":
            r = a + b
        elif t == "-":
            r = a - b
        elif t == "/":
            r = a / b
        elif t == "//":
            r = a // b
        elif t == "%":
            r = a % b
        elif t == "^":
            r = a**b

        stk.append(r)

    return stk.pop()
