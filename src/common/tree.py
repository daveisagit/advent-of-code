"""Tree structures"""


class Node:
    """A generic tree node"""

    def __init__(self, parent, data) -> None:
        self.data = data
        self.parent = parent
        self.children = []
        if isinstance(parent, Node | None):
            if parent:
                parent.children.append(self)
        else:
            raise TypeError("Expected a Node for the parent")

    def __str__(self) -> str:
        return str(self.data)

    def dump(self, indent=0):
        """Quick visual"""
        mrg = 2
        pad = ""
        pic = ""
        if indent > 0:
            pad = " " * (indent - 1) * mrg
            pic = "+" + ("-" * (mrg - 1))
        print(pad + pic + self.data)
        for ch in self.children:
            ch.dump(indent + 1)

    def leaf_nodes(self):
        """Generator for leaf nodes"""
        if not self.children:
            yield self
        for ch in self.children:
            yield from ch.leaf_nodes()

    def ancestors(self):
        """Generator for ancestors"""
        n = self
        while n.parent:
            yield n.parent
            n = n.parent
