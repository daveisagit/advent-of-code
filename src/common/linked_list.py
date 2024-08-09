"""Linked List"""


class Node:
    """Has data but could just act as base class"""

    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


def insert_after_node(after: Node, thing) -> Node:
    """Insert after either a node or some data"""
    node = thing
    if not isinstance(thing, Node):
        node = Node(thing)

    before: Node = after.next

    after.next = node
    node.prev = after

    before.prev = node
    node.next = before

    return node


def find_node(node: Node, data) -> Node:
    """Find a node where data matches"""
    for n in traverse_from_node(node):
        if n.data == data:
            return n
    for n in traverse_from_node(node, forward=False):
        if n.data == data:
            return n
    return None


def traverse_from_node(start: Node, forward=True):
    """Generator for nodes in a list"""
    node = start
    while True:
        if forward:
            node = node.next
        else:
            node = node.prev
        if node:
            yield node
        else:
            break


def remove_node(node: Node, delete=True):
    """Remove this node"""
    prv: Node = node.prev
    nxt: Node = node.next
    if prv:
        prv.next = nxt
    if nxt:
        nxt.prev = prv
    if delete:
        del node
