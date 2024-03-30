"""Tree structures"""


class Node:
    """A generic tree node"""

    def __init__(self, parent, data=None) -> None:
        self.data = data
        self.parent = parent
        self.children = []
        if isinstance(parent, Node | None):
            if parent:
                self.set_parent(parent)
        else:
            raise TypeError("Expected a Node for the parent")

    def __str__(self) -> str:
        return str(self.data)

    def set_parent(self, p):
        """Set the parent"""
        self.parent = p
        p.children.append(self)

    def dump(self, indent=0):
        """Quick visual"""
        mrg = 2
        pad = ""
        pic = ""
        if indent > 0:
            pad = " " * (indent - 1) * mrg
            pic = "+" + ("-" * (mrg - 1))
        print(pad + pic + str(self.data))
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

    def root(self):
        """Get the root node"""
        root = self
        for a in self.ancestors():
            root = a
        return root
