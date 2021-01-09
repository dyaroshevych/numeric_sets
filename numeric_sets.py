from typing import List
from numbers import Number


class Interval:
    def __init__(self, start: int, end: int,
                 is_start_inclusive: bool = False, is_end_inclusive: int = False):
        """
        Initialize a numeric interval with certain range.
        """
        self.start = start
        self.end = end
        self.is_start_inclusive = is_start_inclusive
        self.is_end_inclusive = is_end_inclusive

    def get_formatted(self) -> str:
        """
        Return formatted interval as a string.
        """
        opening_bracket = '[' if self.is_start_inclusive else '('
        closing_bracket = ']' if self.is_end_inclusive else ')'

        return f'{opening_bracket}{self.start}, {self.end}{closing_bracket}'

    def is_overlapping(self, interval) -> bool:
        """
        Determine whether the interval overlaps with the given interval.
        """
        # Check if start of the first interval is to
        # the right from the start of the second interval
        if self.is_start_inclusive and interval.is_start_inclusive:
            start_check_1 = self.start >= interval.start
        else:
            start_check_1 = self.start > interval.start

        # Check if start of the first interval is to
        # the left from the end of the second interval
        if self.is_start_inclusive and interval.is_end_inclusive:
            end_check_1 = self.start <= interval.end
        else:
            end_check_1 = self.start < interval.end

        # Check if start of the second interval is to
        # the right from the start of the first interval
        if interval.is_start_inclusive and self.is_start_inclusive:
            start_check_2 = interval.start >= self.start
        else:
            start_check_2 = interval.start > self.start

        # Check if start of the second interval is to
        # the left from the end of the first interval
        if interval.is_start_inclusive and self.is_end_inclusive:
            end_check_2 = interval.start <= self.end
        else:
            end_check_2 = interval.start < self.end

        return (start_check_1 and end_check_1) or (start_check_2 and end_check_2)

    def is_almost_overlapping(self, interval) -> bool:
        """
        Determine whether the interval almost overlaps with the other interval.
        Two intervals almost overlap if their union forms one interval.
        """
        # If intervals overlap, they are not almost overlapping
        if self.is_overlapping(interval):
            return False

        is_start_junction = self.start == interval.end and (
            self.is_start_inclusive or interval.is_end_inclusive)
        is_end_junction = self.end == interval.start and (
            self.is_end_inclusive or interval.is_start_inclusive)

        return is_start_junction or is_end_junction

    def includes(self, point: Number) -> bool:
        """
        Determine whether the interval includes the given point.
        """
        is_inside = self.start < point < self.end
        is_start = self.is_start_inclusive and self.start == point
        is_end = self.is_end_inclusive and self.end == point

        return is_inside or is_start or is_end

    @ staticmethod
    def intersection(interval_1, interval_2):
        """
        Return an interval that consists of intersection of two given intervals.
        Return None if the result interval is empty.
        """
        start = max(interval_1.start, interval_2.start)
        end = min(interval_1.end, interval_2.end)

        is_start_inclusive = interval_1.includes(
            start) and interval_2.includes(start)
        is_end_inclusive = interval_1.includes(
            end) and interval_2.includes(end)

        if start > end or (start == end and not is_start_inclusive):
            return None

        return Interval(start, end, is_start_inclusive, is_end_inclusive)

    @ staticmethod
    def union(interval_1, interval_2):
        """
        Return a set of intervals that consists of union of two given intervals.
        """
        # Check if the result should consist of two separate intervals.
        if not (interval_1.is_overlapping(interval_2) or interval_1.is_almost_overlapping(interval_2)):
            return Numeric_Set([interval_1, interval_2])

        start = min(interval_1.start, interval_2.start)
        end = max(interval_1.end, interval_2.end)

        is_start_inclusive = interval_1.includes(
            start) or interval_2.includes(start)
        is_end_inclusive = interval_1.includes(
            end) or interval_2.includes(end)

        result = Interval(start, end, is_start_inclusive, is_end_inclusive)

        return Numeric_Set([result])


class Numeric_Set:
    def __init__(self, intervals=[]):
        self.intervals = sorted(intervals, key=lambda interval: interval.start)

    def get_left_intervals(self, interval: Interval) -> List[Interval]:
        """
        Construct a list of intervals that are to the left from the given interval.
        """
        left = []

        for intr in self.intervals:
            if intr.end <= interval.start and not intr.is_almost_overlapping(interval):
                left.append(intr)

        return left

    def get_right_intervals(self, interval: Interval) -> List[Interval]:
        """
        Construct a list of intervals that are to the right from the given interval.
        """
        right = []

        for intr in self.intervals:
            if intr.start >= interval.end and not intr.is_almost_overlapping(interval):
                right.append(intr)

        return right

    def add(self, new_interval: Interval) -> None:
        """
        Add a numeric interval to the set.
        """
        # If there are no other intervals, simply add the interval
        if self.is_empty():
            self.intervals.append(new_interval)
            return

        # If interval should be the leftmost one and does not
        # overlap with the first one, insert it at the start
        if (new_interval.end <= self.intervals[0].start and
                not new_interval.is_overlapping(self.intervals[0]) and
                not new_interval.is_almost_overlapping(self.intervals[0])):
            self.intervals.insert(0, new_interval)
            return

        # If interval should be the right one and does not
        # overlap with the last one, insert it at the start
        if (new_interval.start >= self.intervals[-1].end and
                not new_interval.is_overlapping(self.intervals[-1]) and
                not new_interval.is_almost_overlapping(self.intervals[-1])):
            self.intervals.append(new_interval)
            return

        new_start, new_end = new_interval.start, new_interval.end

        # All intervals located to the left from the new interval
        left = self.get_left_intervals(new_interval)

        # All intervals located to the right from the new interval
        right = self.get_right_intervals(new_interval)

        if left + right != self.intervals:
            new_start = min(new_start, self.intervals[len(left)].start)
            new_end = max(new_end, self.intervals[~len(right)].end)

        is_start_inclusive = (new_interval.start == new_start and new_interval.is_start_inclusive) or (
            (self.intervals[len(left)].start == new_start and self.intervals[len(left)].is_start_inclusive))
        is_end_inclusive = (new_interval.end == new_end and new_interval.is_end_inclusive) or (
            self.intervals[len(left)].end == new_end and self.intervals[len(left)].is_end_inclusive)

        updated_interval = Interval(
            new_start, new_end, is_start_inclusive, is_end_inclusive)

        self.intervals = left + [updated_interval] + right

    def clear(self) -> None:
        """
        Clear the set from all numeric intervals.
        """
        self.intervals = []

    def copy(self):
        """
        Return a copy of the numric set.
        """
        return Numeric_Set([*self.intervals])

    def difference(self, set) -> None:
        """
        Return a set representing a difference
        between the set and the given set.
        """
        updated_set = self.copy()
        updated_set.difference_update(set)

        return updated_set

    def difference_update(self, set) -> None:
        """
        Calculate difference between the set and the
        given set and update the set in-place.
        """
        for interval in set.intervals:
            self.remove(interval)

    def intersection(self, set):
        """
        Return an intersection of the set and the given set.
        """

    def intersection_update(self, set) -> None:
        """
        Calculate intersection of the set and the
        given set and update the set in-place.
        """

    def issubset(self, set) -> bool:
        """
        Determine whether the set is a subset of the given set.
        """
        return set.difference(self).is_empty()

    def issuperset(self, set) -> bool:
        """
        Determine whether the set is a superset of the given set.
        """
        return self.difference(set).is_empty()

    def pop(self) -> Interval:
        """
        Remove the rightmost interval if such exists.
        Otherwise, return None.
        """
        if self.is_empty():
            return None

        return self.intervals.pop()

    # to be finished...
    def remove(self, interval: Interval) -> None:
        """
        Remove a numeric interval from the set.
        """
        # All intervals located to the left from the new interval
        left = self.get_left_intervals(interval)

        # All intervals located to the right from the new interval
        right = self.get_right_intervals(interval)

        self.intervals = left + right

    def symmetric_difference(self, set):
        """
        Return a set with the symmetric differences of two sets.
        """
        return self.difference(set).union(set.difference(self))

    def symmetric_difference_update(self, set):
        """
        Find a set with the symmetric differences of two sets
        and update the set to be equal to it.
        """
        self.intervals = self.difference(set).union(
            set.difference(self)).intervals

    def union(self, set) -> None:
        """
        Return a union of the set and the given set of numeric intervals.
        """
        updated_set = self.copy()
        updated_set.update(set)

        return updated_set

    def update(self, set) -> None:
        """
        Find a union of the set and the given set of numeric intervals
        and update the set to be equal to it.
        """
        for interval in set.intervals:
            self.add(interval)

    def is_empty(self) -> bool:
        """
        Determine whether a set of intervals is empty.
        """
        return len(self.intervals) == 0

    def save(self, filename: str = 'result.txt') -> None:
        """
        Save a set of numeric intervals in the given file.
        The default filename is 'results.txt'.
        """
        with open(filename, 'w') as output_file:
            for interval in self.intervals:
                output_file.write(interval.get_formatted() + '\n')

    @ staticmethod
    def read(filename: str) -> List[Interval]:
        """
        Read a set of numerical intervals from the given file.
        """
        intervals = []

        with open(filename, 'r') as input_file:
            for raw_interval in input_file.readlines():
                # remove '\n' at the end of the line
                raw_interval = raw_interval.rstrip()

                if not raw_interval:
                    continue

                start, end = map(int, raw_interval[1:-1].split(', '))

                is_start_inclusive = raw_interval[0] == '['
                is_end_inclusive = raw_interval[-1] == ']'

                intervals.append(
                    Interval(start, end, is_start_inclusive, is_end_inclusive))

        return intervals
