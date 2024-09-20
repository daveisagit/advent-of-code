class Node:
    """Represents an element of a set."""

    def __init__(self, id):
        self.id = id
        self.parent = self
        self.rank = 0
        self.size = 1

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return "Node({!r})".format(self.id)


def find(x):
    """Returns the representative object of the set containing x."""
    if x.parent is not x:
        x.parent = find(x.parent)
    return x.parent


def union(x, y):
    """Combines the sets x and y belong to."""
    x_root = find(x)
    y_root = find(y)

    # x and y are already in the same set
    if x_root is y_root:
        return

    # x and y are not in same set, so we merge them
    if x_root.rank < y_root.rank:
        x_root, y_root = y_root, x_root

    # merge
    y_root.parent = x_root
    x_root.size += y_root.size
    if x_root.rank == y_root.rank:
        x_root.rank = x_root.rank + 1


# x = Node("fred")
# print(x)
# print(repr(x))
