"""String and list tools"""

from collections import deque
import hashlib
from itertools import chain, combinations
import json


def get_column(data, col: int) -> list:
    """Return a column of data"""
    return [row[col] for row in data]


def tok(in_str: str, delim=" ") -> list:
    """Tokenize i.e. split and strip"""
    return [e.strip() for e in in_str.split(delim)]


def window_over(iterable, width: int, step=1):
    """Generator of windows over an iterable"""
    for idx in range(0, len(iterable) - width + 1, step):
        yield iterable[idx : idx + width]


def sign(n) -> int:
    """Returns -1, 0, or 1"""
    if n == 0:
        return 0
    if n > 0:
        return 1
    return -1


#
# not used
#


def get_alpha_value(item: str):
    """the value of an item a=1 ...  z=26 , A=27 , etc .."""
    if item.islower():
        return ord(item) - 96
    return ord(item) - 38


def split_into_groups(a_list: list, size: int) -> list:
    """Split a list into groups of a fixed size"""
    for idx in range(0, len(a_list), size):
        yield a_list[idx : idx + size]


def reverse_string(in_str: str) -> str:
    """Python reversing by slices"""
    return in_str[::-1]


def hex_pad(dec: int, length: int) -> str:
    """Convert dec to hex padded with zero"""
    s = hex(dec)[2:]
    p = length - len(s)
    p = ["0"] * p
    p = "".join(p)
    return p + s


def powerset(iterable):
    """Return the powerset of an iterable
    for example powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"""
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def dict_hash(d) -> str:
    """MD5 hash of a dictionary."""
    dh = hashlib.md5()
    # We need to sort arguments so {'a': 1, 'b': 2} is
    # the same as {'b': 2, 'a': 1}
    encoded = json.dumps(d, sort_keys=True).encode()
    dh.update(encoded)
    return dh.hexdigest()


def find_sublists(lst, max_occur=None, min_size=1, max_size=None):
    """Return a list of list that would cover the whole list for any
    arrangement and re-se of the sublists"""

    def remove_state():
        wl = lst.copy()
        for sl in state:
            # remove all occurrences of sl from wl
            removing = True
            while removing:
                removing = False
                for p, w in enumerate(window_over(wl, len(sl))):
                    if w == sl:
                        wl = wl[:p] + wl[p + len(sl) :]
                        removing = True
                        break
        return wl

    if max_occur is None:
        max_occur = len(lst)
    if max_size is None:
        max_size = len(lst)

    dfs = deque()
    dfs.append([])
    while dfs:
        state = dfs.pop()
        wl = remove_state()
        if not wl:
            if len(state) <= max_occur:
                return state

        for s in range(min_size, min(max_size, len(wl))):
            t = wl[:s]
            ns = state.copy()
            ns.append(t)
            dfs.append(ns)

    return None


def test_sublists():
    """From 2019 Day 17"""
    l = (
        "L,6,R,12,R,8,R,8,R,12,L,12,R,8,R,12,"
        "L,12,L,6,R,12,R,8,R,12,L,12,L,4,L,4,L,6,"
        "R,12,R,8,R,12,L,12,L,4,L,4,L,6,R,12,R,8,"
        "R,12,L,12,L,4,L,4,R,8,R,12,L,12"
    )
    l = l.split(",")
    sl = find_sublists(l, 3, min_size=4, max_size=10)
    print(sl)


def powerset_swap(set_size):
    """Generator for an index to add/remove that will take you through
    all the powerset combinations from any state"""
    for x in range(1, 2**set_size):
        t = x
        b = 0
        while t % 2 == 0:
            b += 1
            t = t >> 1
        yield b


def test_powerset_swap():
    """Test powerset_swap"""

    def run_swap():
        for idx in powerset_swap(len(l)):
            c = l[idx]
            if c in s:
                s.remove(c)
            else:
                s.add(c)
            print(s)

    l = list("ABCD")
    s = set(l)
    print(f"Start full {s}")
    run_swap()
    s = set(["A", "C"])
    print(f"Start {s}")
    run_swap()
