"""Multi-dimensional blocks"""

from bisect import bisect_left
from collections import defaultdict
from itertools import pairwise
from blocksets import Block


class BlockResolverUsingBlock:
    """Resolve operations on blocks"""

    def __init__(self, dimensions, _cross_section_resolver) -> None:
        self._dimensions = dimensions
        self._operation_stack = []
        self._marker_ordinates = []
        self._marker_stack = []
        self._dimension_segment_usage_count = []
        self._cross_section_resolver = _cross_section_resolver

    def _refresh_marker_ordinates(self):
        """Refreshes _marker_ordinates which stores actual ordinate values of
        the grid markers"""

        self._marker_ordinates.clear()
        for d in range(self._dimensions):
            markers = set()
            for block_operation in self._operation_stack:
                block: Block = block_operation[0]
                markers.add(block.a[d])
                markers.add(block.b[d])
            markers = list(sorted(markers))
            self._marker_ordinates.append(markers)

    def _refresh_marker_stack(self):
        """Refreshes _marker_stack which is equivalent to _operation_stack but
        expressed as grid markers instead of the block ordinates"""

        self._marker_stack.clear()
        for block, stack_data in self._operation_stack:
            a = []
            b = []
            for d in range(self._dimensions):
                markers = self._marker_ordinates[d]
                a.append(bisect_left(markers, block.a[d]))
                b.append(bisect_left(markers, block.b[d]))
            marker_block = (tuple(a), tuple(b))
            entry = (marker_block, stack_data)
            self._marker_stack.append(entry)

    def _refresh_dimension_segment_usage_counts(self):
        self._dimension_segment_usage_count = []
        for d in range(self._dimensions):
            segment_usage_count = defaultdict(set)
            for idx, (blk, _) in enumerate(self._marker_stack):
                a = blk[0][d]
                b = blk[1][d]
                for x in range(a, b):
                    segment_usage_count[x].add(idx)
            segment_usage_count = sorted(
                segment_usage_count.items(), key=lambda x: len(x[1]), reverse=True
            )
            self._dimension_segment_usage_count.append(segment_usage_count)

    def _resolve_recursively(self, marker_stack: list, dimension: int = 0) -> dict:
        """Scan and resolve"""

        # Being in the last dimension is a special case so we note it up front
        last_dimension = False
        if self._dimensions == dimension + 1:
            last_dimension = True

        # Final result set
        resolved_blocks = {}

        # Used to handle the changes found in cross sections as scan through
        prev_resolved_x_sec = {}
        change_marker = None

        # For each marker in this dimension we get the cross section of
        # normalised blocks of the lower dimension.

        # If there is a change in the normalised blocks between cross sections
        # then this indicates we should create blocks in this dimension and add
        # them to our result set.

        for m in range(len(self._marker_ordinates[dimension])):

            # Get the operation stack for the lower dimension at this marker
            # If this is the last dimension then only the operation makes sense
            cross_section = [
                (
                    (None, stack_data)
                    if last_dimension
                    else (
                        (blk[0][1:], blk[1][1:]),
                        stack_data,
                    )
                )
                for blk, stack_data in marker_stack
                if blk[0][0] <= m < blk[1][0]
            ]

            if last_dimension:

                resolved_x_sec = self._cross_section_resolver(cross_section)

            else:
                # Get the normalised representation of this cross section
                # using recursion
                resolved_x_sec = self._resolve_recursively(cross_section, dimension + 1)

            # By only adding blocks when there are cross section changes
            # we should hopefully remove redundant blocks
            if resolved_x_sec != prev_resolved_x_sec:

                # if the change_marker is None then we have
                # not got a previous x-section
                if change_marker is not None:

                    # the last dimension simply means we set the value
                    # for 1D interval (if we have a value of worth)
                    if last_dimension and prev_resolved_x_sec:
                        resolved_blocks[((change_marker,), (m,))] = prev_resolved_x_sec

                    # otherwise for all other dimensions
                    # we use the value from the previous x-section
                    # to construct the block in this dimension
                    if not last_dimension:
                        for x, v in prev_resolved_x_sec.items():
                            a = (change_marker,) + x[0]
                            b = (m,) + x[1]
                            resolved_blocks[(a, b)] = v

                change_marker = m
                prev_resolved_x_sec = resolved_x_sec

        return resolved_blocks

    def resolve(self):
        """Normalise the Block operations"""

        def markers_to_ordinates(marker_tuple):
            return tuple(
                self._marker_ordinates[d][m] for d, m in enumerate(marker_tuple)
            )

        self._refresh_marker_ordinates()
        self._refresh_marker_stack()

        resolved_markers = self._resolve_recursively(self._marker_stack)

        # replace the operation stack with ADD operations for the normalised result
        self._operation_stack = [
            (
                Block(*tuple(markers_to_ordinates(x) for x in marker_block)),
                (value, "+"),
            )
            for marker_block, value in resolved_markers.items()
        ]

    def most_intersected_segments(self, top=1):
        """Returns a list of the most heavily used segments within
        the marker space"""

        def read_dimension(d, all_indexes=None, segments=()):
            nonlocal most_intersected
            bar_level = 0
            if len(most_intersected) >= top:
                bar_level = most_intersected[top - 1][1]

            for dimension_count in self._dimension_segment_usage_count[d]:
                seg = dimension_count[0]
                indexes = dimension_count[1]
                if d == 0:
                    new_all_indexes = indexes
                else:
                    new_all_indexes = all_indexes & indexes
                if len(new_all_indexes) < bar_level:
                    return

                segments += (seg,)
                if d < self._dimensions - 1:
                    read_dimension(
                        d + 1, all_indexes=new_all_indexes, segments=segments
                    )
                else:
                    if len(new_all_indexes) >= bar_level:
                        most_intersected.append((segments, len(new_all_indexes)))
                        most_intersected = sorted(
                            most_intersected, key=lambda x: x[1], reverse=True
                        )
                        if len(most_intersected) >= top:
                            bar_level = most_intersected[top - 1][1]

        most_intersected = []
        self._refresh_dimension_segment_usage_counts()
        read_dimension(0)
        return most_intersected


class BlockResolver:
    """Resolve operations on blocks"""

    def __init__(self, dimensions, _cross_section_resolver) -> None:
        self._dimensions = dimensions
        self._operation_stack = []
        self._marker_ordinates = []
        self._marker_stack = []
        self._dimension_segment_usage_count = []
        self._cross_section_resolver = _cross_section_resolver

    def _refresh_marker_ordinates(self):
        """Refreshes _marker_ordinates which stores actual ordinate values of
        the grid markers"""

        self._marker_ordinates.clear()
        for d in range(self._dimensions):
            markers = set()
            for block_operation in self._operation_stack:
                block = block_operation[0]
                markers.add(block[0][d])
                markers.add(block[1][d])
            markers = list(sorted(markers))
            self._marker_ordinates.append(markers)

    def _refresh_marker_stack(self):
        """Refreshes _marker_stack which is equivalent to _operation_stack but
        expressed as grid markers instead of the block ordinates"""

        self._marker_stack.clear()
        for block, stack_data in self._operation_stack:
            a = []
            b = []
            for d in range(self._dimensions):
                markers = self._marker_ordinates[d]
                a.append(bisect_left(markers, block[0][d]))
                b.append(bisect_left(markers, block[1][d]))
            marker_block = (tuple(a), tuple(b))
            entry = (marker_block, stack_data)
            self._marker_stack.append(entry)

    def _refresh_dimension_segment_usage_counts(self):
        self._dimension_segment_usage_count = []
        for d in range(self._dimensions):
            segment_usage_count = defaultdict(set)
            for idx, (blk, _) in enumerate(self._marker_stack):
                a = blk[0][d]
                b = blk[1][d]
                for x in range(a, b):
                    segment_usage_count[x].add(idx)
            segment_usage_count = sorted(
                segment_usage_count.items(), key=lambda x: len(x[1]), reverse=True
            )
            self._dimension_segment_usage_count.append(segment_usage_count)

    def _resolve_recursively(self, marker_stack: list, dimension: int = 0) -> dict:
        """Scan and resolve"""

        # Being in the last dimension is a special case so we note it up front
        last_dimension = False
        if self._dimensions == dimension + 1:
            last_dimension = True

        # Final result set
        resolved_blocks = {}

        # Used to handle the changes found in cross sections as scan through
        prev_resolved_x_sec = {}
        change_marker = None

        # For each marker in this dimension we get the cross section of
        # normalised blocks of the lower dimension.

        # If there is a change in the normalised blocks between cross sections
        # then this indicates we should create blocks in this dimension and add
        # them to our result set.

        for m in range(len(self._marker_ordinates[dimension])):

            # Get the operation stack for the lower dimension at this marker
            # If this is the last dimension then only the operation makes sense
            cross_section = [
                (
                    (None, stack_data)
                    if last_dimension
                    else (
                        (blk[0][1:], blk[1][1:]),
                        stack_data,
                    )
                )
                for blk, stack_data in marker_stack
                if blk[0][0] <= m < blk[1][0]
            ]

            if last_dimension:

                resolved_x_sec = self._cross_section_resolver(cross_section)

            else:
                # Get the normalised representation of this cross section
                # using recursion
                resolved_x_sec = self._resolve_recursively(cross_section, dimension + 1)

            # By only adding blocks when there are cross section changes
            # we should hopefully remove redundant blocks
            if resolved_x_sec != prev_resolved_x_sec:

                # if the change_marker is None then we have
                # not got a previous x-section
                if change_marker is not None:

                    # the last dimension simply means we set the value
                    # for 1D interval (if we have a value of worth)
                    if last_dimension and prev_resolved_x_sec:
                        resolved_blocks[((change_marker,), (m,))] = prev_resolved_x_sec

                    # otherwise for all other dimensions
                    # we use the value from the previous x-section
                    # to construct the block in this dimension
                    if not last_dimension:
                        for x, v in prev_resolved_x_sec.items():
                            a = (change_marker,) + x[0]
                            b = (m,) + x[1]
                            resolved_blocks[(a, b)] = v

                change_marker = m
                prev_resolved_x_sec = resolved_x_sec

        return resolved_blocks

    def resolve(self):
        """Normalise the Block operations"""

        def markers_to_ordinates(marker_tuple):
            return tuple(
                self._marker_ordinates[d][m] for d, m in enumerate(marker_tuple)
            )

        self._refresh_marker_ordinates()
        self._refresh_marker_stack()

        resolved_markers = self._resolve_recursively(self._marker_stack)

        # replace the operation stack with ADD operations for the normalised result
        self._operation_stack = [
            (
                tuple(markers_to_ordinates(x) for x in marker_block),
                (value, "+"),
            )
            for marker_block, value in resolved_markers.items()
        ]

    def most_intersected_segments(self, top=1):
        """Returns a list of the most heavily used segments within
        the marker space"""

        def read_dimension(d, all_indexes=None, segments=()):
            nonlocal most_intersected
            bar_level = 0
            if len(most_intersected) >= top:
                bar_level = most_intersected[top - 1][1]

            for dimension_count in self._dimension_segment_usage_count[d]:
                seg = dimension_count[0]
                indexes = dimension_count[1]
                if d == 0:
                    new_all_indexes = indexes
                else:
                    new_all_indexes = all_indexes & indexes
                if len(new_all_indexes) < bar_level:
                    return

                segments += (seg,)
                if d < self._dimensions - 1:
                    read_dimension(
                        d + 1, all_indexes=new_all_indexes, segments=segments
                    )
                else:
                    if len(new_all_indexes) >= bar_level:
                        most_intersected.append((segments, len(new_all_indexes)))
                        most_intersected = sorted(
                            most_intersected, key=lambda x: x[1], reverse=True
                        )
                        if len(most_intersected) >= top:
                            bar_level = most_intersected[top - 1][1]

        most_intersected = []
        self._refresh_dimension_segment_usage_counts()
        read_dimension(0)
        return most_intersected


def combine_blocks(a: list, b: list) -> list:
    """A block is a list of dimension pairs (Bx,B'x), (By,B'y), (Bz,B'z)
    where B and B' are the opposite corners. Each pair is like a side of a block.
    The return is a set of blocks which represent the resulting possible workspace
    The client of this function can then determine the relevance of each
    within its own context.
    """
    result = []
    grid_markers = [sorted(set(list(sides[0]) + list(sides[1]))) for sides in zip(a, b)]
    dimensions = len(grid_markers)

    def iterate_dimension(other_sides: list):
        cur_depth = len(other_sides)
        markers = grid_markers[cur_depth]
        for side in pairwise(markers):
            new_list_of_sides = other_sides + [side]
            if cur_depth < dimensions - 1:
                iterate_dimension(new_list_of_sides)
                continue
            result.append(tuple(new_list_of_sides))

    iterate_dimension([])

    return result


def intersection_block(a: list, b: list) -> list:
    """Intersection: of the workspace which new sub blocks are in a and b
    Should be 1 or 0 in theory?"""
    result = []
    for c in combine_blocks(a, b):
        c_inside_a = all(
            a_side[0] <= c_side[0] and c_side[1] <= a_side[1]
            for a_side, c_side in zip(a, c)
        )
        c_inside_b = all(
            b_side[0] <= c_side[0] and c_side[1] <= b_side[1]
            for b_side, c_side in zip(b, c)
        )
        if c_inside_a and c_inside_b:
            result.append(c)
    return result


def test_intersection_block():
    """Test intersection_block"""
    a = ((1, 5), (3, 7))  # 1 @ 1,3: 4x4
    b = ((3, 7), (1, 5))  # 2 @ 3,1: 4x4
    c = ((5, 7), (5, 7))  # 3 @ 5,5: 2x2
    assert intersection_block(a, b) == [((3, 5), (3, 5))]
    assert intersection_block(a, c) == []
    assert intersection_block(b, c) == []


test_intersection_block()
