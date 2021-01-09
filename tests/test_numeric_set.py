"""Test NumericSet class methods from the 'numeric_sets' module using unittest."""


import unittest
from numeric_sets.main import Interval, Numeric_Set


class TestAdd(unittest.TestCase):
    def test_regular(self):
        myset = Numeric_Set()
        myset.add(Interval(2, 3))  # (2, 3)
        myset.add(Interval(13, 15))  # (13, 15)
        myset.add(Interval(9, 10))  # (9, 10)
        myset.add(Interval(6, 8))  # (6, 8)
        myset.add(Interval(0, 1))  # (0, 1)
        myset.add(Interval(2.5, 8.5, is_end_inclusive=True))  # (2.5, 8.5]

        # result: (0, 1) (2, 8.5] (9, 10) (13, 15)
        self.assertEqual(len(myset.intervals), 4)
        self.assertEqual(myset.intervals[0].get_formatted(), '(0, 1)')
        self.assertEqual(myset.intervals[1].get_formatted(), '(2, 8.5]')
        self.assertEqual(myset.intervals[2].get_formatted(), '(9, 10)')
        self.assertEqual(myset.intervals[3].get_formatted(), '(13, 15)')

    def test_empty(self):
        myset = Numeric_Set()
        myset.add(Interval(2, 3))  # (2, 3)

        self.assertEqual(len(myset.intervals), 1)

    def test_start_overlapping_negative(self):
        myset = Numeric_Set()
        myset.add(Interval(2, 3))  # (2, 3)
        myset.add(Interval(1, 2))  # (1, 2)

        self.assertEqual(len(myset.intervals), 2)
        self.assertEqual(myset.intervals[0].get_formatted(), '(1, 2)')
        self.assertEqual(myset.intervals[1].get_formatted(), '(2, 3)')

    def test_start_overlapping_positive(self):
        myset = Numeric_Set()
        myset.add(Interval(2, 3))  # (2, 3)
        myset.add(Interval(1, 2, is_end_inclusive=True))  # (1, 2]

        self.assertEqual(len(myset.intervals), 1)
        self.assertEqual(myset.intervals[0].get_formatted(), '(1, 3)')

    def test_end_overlapping_negative(self):
        myset = Numeric_Set()
        myset.add(Interval(1, 2))  # (1, 2)
        myset.add(Interval(2, 3))  # (2, 3)

        self.assertEqual(len(myset.intervals), 2)
        self.assertEqual(myset.intervals[0].get_formatted(), '(1, 2)')
        self.assertEqual(myset.intervals[1].get_formatted(), '(2, 3)')

    def test_end_overlapping_positive(self):
        myset = Numeric_Set()
        myset.add(Interval(1, 2, is_end_inclusive=True))  # (1, 2]
        myset.add(Interval(2, 3))  # (2, 3)

        self.assertEqual(len(myset.intervals), 1)
        self.assertEqual(myset.intervals[0].get_formatted(), '(1, 3)')


class TestLeftIntervals(unittest.TestCase):
    def test_empty(self):
        myset = Numeric_Set()
        myset.add(Interval(1, 2))  # (1, 2)
        myset.add(Interval(2, 3))  # (2, 3)

        left_intervals = myset.get_left_intervals(Interval(0, 1.5))

        self.assertEqual(len(left_intervals), 0)

    def test_ordinary(self):
        myset = Numeric_Set()
        myset.add(Interval(1, 2))  # (1, 2)
        myset.add(Interval(2, 3))  # (2, 3)
        myset.add(Interval(4, 5))  # (4, 5)

        left_intervals = myset.get_left_intervals(Interval(3, 4))

        self.assertEqual(len(left_intervals), 2)


class TestRightIntervals(unittest.TestCase):
    def test_empty(self):
        myset = Numeric_Set()
        myset.add(Interval(1, 2))  # (1, 2)
        myset.add(Interval(2, 3))  # (2, 3)

        right_intervals = myset.get_right_intervals(Interval(1.5, 2.5))

        self.assertEqual(len(right_intervals), 0)

    def test_ordinary(self):
        myset = Numeric_Set()
        myset.add(Interval(1, 2))  # (1, 2)
        myset.add(Interval(2, 3))  # (2, 3)
        myset.add(Interval(4, 5))  # (4, 5)

        right_intervals = myset.get_right_intervals(Interval(3, 4))

        self.assertEqual(len(right_intervals), 1)


class TestClear(unittest.TestCase):
    def test_ordinary(self):
        myset = Numeric_Set()
        myset.add(Interval(1, 2))
        myset.add(Interval(2, 3))

        myset.clear()

        self.assertEqual(len(myset.intervals), 0)


class TestCopy(unittest.TestCase):
    def test_ordinary(self):
        myset = Numeric_Set()
        myset.add(Interval(1, 2))
        myset.add(Interval(2, 3))

        copy = myset.copy()

        self.assertEqual(copy.intervals[0].get_formatted(
        ), myset.intervals[0].get_formatted())
        self.assertEqual(copy.intervals[1].get_formatted(
        ), myset.intervals[1].get_formatted())


if __name__ == '__main__':
    unittest.main()
