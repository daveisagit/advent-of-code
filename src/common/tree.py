"""Tree structures"""

from collections import defaultdict


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

    @property
    def depth(self):
        """The depth"""
        if self.parent is None:
            return 0
        return self.parent.depth + 1

    def set_parent(self, p):
        """Set the parent"""
        self.parent = p
        p.children.append(self)

    def add_child(self, c):
        """Add a child"""
        self.children.append(c)
        c.parent = self

    def dump(self, indent=0, attrs=None):
        """Quick visual"""
        mrg = 2
        pad = ""
        pic = ""
        if indent > 0:
            pad = " " * (indent - 1) * mrg
            pic = "+" + ("-" * (mrg - 1))
        render = self.data
        if attrs:
            if isinstance(attrs, str):
                render = str(getattr(self, attrs))
            if isinstance(attrs, (list, set, tuple)):
                render = [str(getattr(self, a)) for a in attrs]
                render = " ".join(render)

        print(pad + pic + render)
        for ch in self.children:
            ch.dump(indent + 1, attrs=attrs)

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

    def traverse(self):
        """Traverse from here"""
        yield self
        for c in self.children:
            yield from c.traverse()

    def lowest_common_ancestor(self, n):
        """Return the lowest common ancestor"""
        mine = set(self.ancestors())
        for a in n.ancestors():
            if a in mine:
                return a
        return None

    def path_to(self, n):
        """Return the path from here to there"""
        lca = self.lowest_common_ancestor(n)
        p1 = []
        for a in self.ancestors():
            if a == lca:
                break
            p1.append(a)
        p2 = []
        for a in n.ancestors():
            if a == lca:
                break
            p2.append(a)

        return p1 + [lca] + list(reversed(p2))


def make_tree(data):
    """Given a dict of IDs and iter (i.e. a graph)
    p_id : { c_id_1, c_id_2, ... }
    Return a dict of nodes"""

    def get_node(n_id):
        if n_id not in nodes:
            n = Node(None, n_id)
            nodes[n_id] = n
        return nodes[n_id]

    nodes = {}

    for p, cs in data.items():
        pn = get_node(p)
        for c in cs:
            cn = get_node(c)
            cn.set_parent(pn)

    return nodes


def edges_to_graph(edges):
    """Return a graph given an iterator of (parent,child) tuple"""
    gph = defaultdict(dict)
    for p, c in edges:
        gph[p][c] = 1
    return gph
