"""Useful functions for when dealing with intervals
(lower bound , upper bound) like a python slice where
the lower bound is included
the upper bound is excluded

Interval objects are immutable (like tuples)

Interval methods receiving another Interval object as an argument include:

    - Tests against another interval returning a boolean:
        borders, overlaps, surrounds, surrounded_by, could_merge

    - A result of interaction with another interval returning a new interval object
        merge, gap, overlap
    
    - A result of interaction with another interval returning a set of new interval objects
        remove (this returns a set as we could remove a section in the middle 
        leaving 2 intervals as a result)

Interval Set functions all return a set of intervals objects
( isolated intervals: are a set of intervals that do not overlap or border any others in the set )

    - Functions with a single set argument:
        normalise (removes redundant entries to return a set of isolated intervals)

    - Functions with a single set argument and a second single 
      interval argument (notionally a window/range)
        crop, mergable_intervals, negation

    - Functions acting as a binary operation on 2 sets of intervals:
        union, intersection, minus

"""

from typing import Self


class Interval:
    """Objects are immutable (so they can be hashed for usage in sets)"""

    def __init__(self, start: int, end: int) -> None:
        if start == end:
            raise ValueError(
                f"The start and end values {start} can not be the same, it's a null interval"
            )
        self._start = start
        self._end = end
        if start > end:
            self._start = end
            self._end = start

    @property
    def start(self) -> int:
        """Immutable start"""
        return self._start

    @property
    def end(self) -> int:
        """Immutable end"""
        return self._end

    def __hash__(self) -> int:
        """Make use of the hashing used by tuples"""
        return hash((self._start, self._end))

    def __repr__(self) -> str:
        """Represent as a tuple"""
        return str(self.tuple())

    def __eq__(self, __value: object) -> bool:
        """Compare as a tuple"""
        return self.tuple() == __value

    def tuple(self) -> tuple:
        """tuple format"""
        return (self.start, self.end)

    def size(self) -> int:
        """Return interval size"""
        return abs(self.end - self.start)

    def borders(self, i: Self) -> bool:
        """Return true if the intervals touch exactly on a boundary"""
        if self.start == i.end or self.end == i.start:
            return True
        return False

    def overlaps(self, i: Self) -> bool:
        """Return true if the intervals overlap in any way"""
        if self.start <= i.start and self.end > i.start:
            return True
        if i.start <= self.start and i.end > self.start:
            return True
        return False

    def surrounds(self, i: Self) -> bool:
        """Return true if this surrounds the given"""
        if self.start <= i.start and self.end >= i.end:
            return True
        return False

    def surrounded_by(self, i: Self) -> bool:
        """Return true if this is surrounded by the given"""
        if i.start <= self.start and i.end >= self.end:
            return True
        return False

    def could_merge(self, i: Self) -> bool:
        """Return true if the intervals overlap or border each other"""
        if self.borders(i) or self.overlaps(i):
            return True
        return False

    def merge(self, i: Self) -> Self | None:
        """Return a new interval object as the result of merging 2 overlapping ones"""
        if not self.could_merge(i):
            return None
        return Interval(min(self.start, i.start), max(self.end, i.end))

    def gap(self, i: Self) -> Self | None:
        """Return a new interval object as the result of the gap between 2"""
        if self.could_merge(i):
            return None
        return Interval(min(self.end, i.end), max(self.start, i.start))

    def overlap(self, i: Self) -> Self | None:
        """Return a new interval cropping the limits to the given"""
        if not self.overlaps(i):
            return None
        return Interval(max(self.start, i.start), min(self.end, i.end))

    def remove(self, i: Self) -> set[Self]:
        """Return a set of new intervals with the overlap removed
        The set will have 0,1 or 2 intervals"""
        if i.surrounds(self):
            return set()
        overlap = self.overlap(i)
        if not overlap:
            return {self}

        result = set()
        if self.start < i.start:
            result.add(Interval(self.start, i.start))
        if i.end < self.end:
            result.add(Interval(i.end, self.end))

        return result

    def copy(self, adj: int = 0) -> Self:
        """Return a copy (possibly translated)"""
        return Interval(self.start + adj, self.end + adj)


#
# functions for handling sets of Intervals
#


def covering_interval(intervals: set[Interval]) -> Interval:
    """Returns the minimum interval that covers the set"""
    start = min([i.start for i in intervals])
    end = max([i.end for i in intervals])
    return Interval(start, end)


def crop(intervals: set[Interval], cropping_interval: Interval) -> set[Interval]:
    """Returns a new set but cropped at the limits"""
    res = set()
    for i in intervals:
        if cropping_interval.surrounds(i):
            res.add(i)
            continue
        if cropping_interval.overlaps(i):
            res.add(i.overlap(cropping_interval))
    return res


def mergable_intervals(intervals: set[Interval], given: Interval) -> set[Interval]:
    """Return a set of intervals that could be merged with the given one
    ignoring itself of course.

    Primarily for use by the mergability function but might also be useful outside that context
    """
    res = set()
    for i in intervals:
        if i == given:
            continue
        if i.could_merge(given):
            res.add(i)
    return res


def mergability(intervals: set[Interval]) -> tuple[set[Interval]]:
    """Returns 2 sets,
    - a subset of intervals that are isolated
    - a subset of intervals that are not isolated

    Primarily for use by the normalize function but may be of use outside of that"""
    isolated = set()
    mergable = set()

    for interval in intervals:
        if mergable_intervals(intervals, interval):
            mergable.add(interval)
        else:
            isolated.add(interval)

    return isolated, mergable


def normalize(intervals: set[Interval]) -> set[Interval]:
    """Returns a set of isolated intervals covering the same space
    (a merge or squash if you like)"""
    isolated: set
    mergable: set
    result: set
    result, mergable = mergability(intervals)
    while mergable:
        print(len(mergable))
        # find 2 mergable intervals in the mergable set
        interval_a: Interval = mergable.pop()
        interval_b: Interval = None
        for other in mergable:
            if interval_a == other:
                continue
            if interval_a.could_merge(other):
                interval_b = other
                break

        # both are removed and replaced by a single interval
        mergable.remove(interval_b)
        merged_interval = interval_a.merge(interval_b)
        mergable.add(merged_interval)

        # iterate until we only have isolated intervals
        isolated, mergable = mergability(mergable)
        result.update(isolated)

    return result


def union(set_a: set[Interval], set_b: set[Interval]) -> set[Interval]:
    """Returns a normalized union of 2 interval sets"""
    result = set_a.copy()
    result.update(set_b)
    result = normalize(result)
    return result


def intersection(set_a: set[Interval], set_b: set[Interval]) -> set[Interval]:
    """Returns a normalized intersection of 2 interval sets
    Effectively a cross product to create all possible overlaps and
    then normalised union of the result gives the overall intersection
    """
    result = set()
    for interval_a in set_a:
        for interval_b in set_b:
            overlap = interval_a.overlap(interval_b)
            if overlap:
                result.add(overlap)
    result = normalize(result)
    return result


def ordered_list(intervals: set[Interval]) -> list[Interval]:
    """Returns the set normalized and in an ordered list
    Primarily for negation, but available for general use"""
    intervals = normalize(intervals)
    sorted_intervals = sorted(list(intervals), key=lambda x: x.start)
    return sorted_intervals


def negation(intervals: set[Interval], window: Interval) -> set[Interval]:
    """Returns the inverse or negative as a new set (limits defined by the given window)
    Primarily for use by the minus function, but available generally"""
    intervals = crop(normalize(intervals), window)

    if not intervals:
        # if there are no intervals in the window
        # then result is the window (set of 1)
        return {window}

    inverse = set()
    sorted_intervals = ordered_list(intervals)

    # add all the gaps in between
    for idx in range(len(sorted_intervals) - 1):
        interval_a = sorted_intervals[idx]
        interval_b = sorted_intervals[idx + 1]
        gap = interval_a.gap(interval_b)
        inverse.add(gap)

    # then a possible gap at the start
    if window.start < sorted_intervals[0].start:
        inverse.add(Interval(window.start, sorted_intervals[0].start))

    # and at the end
    if window.end > sorted_intervals[-1].end:
        inverse.add(Interval(sorted_intervals[-1].end, window.end))

    return inverse


def minus(set_a: set[Interval], set_b: set[Interval]) -> set[Interval]:
    """Returns a normalized result of A - B

    Since:
       A - B   <=>   A and ~B

    We make use of the negation function on B and intersect it with A
    ( the ~B is scoped/windowed by the coverage of A as anything outside of A is not relevant )
    """
    set_a = normalize(set_a)
    window = covering_interval(set_a)
    neg_b = negation(set_b, window)
    result = intersection(set_a, neg_b)
    return result
