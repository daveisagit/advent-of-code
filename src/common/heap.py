"""Minimum Binary Heap

A wrapper for heapq which will effectively give us the ability to update an entry.

This is done by holding the current value in a dictionary.

Any entries on the actual heap that do not match are ignored (and removed upon discovery).

So we can push a new value for a key without worrying about removing the old one.

When pushing onto the heap the value is placed as the first in a tuple and the 
second term is just a counter to ensure FIFO if values are equal

Methods

get(key):           return the value
min():              return the top as a tuple (key,value)
pop():              return the top as a tuple (key,value) & remove it
upsert(key,value):  returns a boolean for success. 
As there is the option of allow_increase. By default this is false
and will protect from updates if the value increases and return false

"""

from heapq import heappop, heappush
from itertools import count


class BinaryHeap:
    """A binary heap."""

    def __init__(self):
        """Initialize a binary heap."""
        super().__init__()
        self._dict = {}
        self._heap = []
        self._count = count()

    def min(self):
        """Return the top the heap (without removal)"""
        dct = self._dict
        if not dct:
            raise ValueError("heap is empty")
        heap = self._heap
        pop = heappop
        # remove stale entries
        while True:
            value, _, key = heap[0]
            if key in dct and value == dct[key]:
                break
            pop(heap)
        return (key, value)

    def pop(self):
        """Return the top the heap (with removal)"""
        dct = self._dict
        if not dct:
            raise ValueError("heap is empty")
        heap = self._heap
        pop = heappop
        # remove stale entries
        while True:
            value, _, key = heap[0]
            pop(heap)
            if key in dct and value == dct[key]:
                break
        del dct[key]
        return (key, value)

    def get(self, key, default=None):
        """Simple getter"""
        return self._dict.get(key, default)

    def upsert(self, key, value, allow_increase=False):
        """Think of it as an update or push, returns True if it did add or update"""
        dct = self._dict
        if key in dct:
            old_value = dct[key]
            if value < old_value or (allow_increase and value > old_value):
                dct[key] = value
                heappush(self._heap, (value, next(self._count), key))
                return value < old_value
            return False

        # new entry
        dct[key] = value
        heappush(self._heap, (value, next(self._count), key))
        return True
