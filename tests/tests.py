"""Test classes methods from the 'numeric_sets' module using unittest."""


import unittest
from numeric_sets import Interval, Numeric_Set


class TestIntervalFormat(unittest.TestCase):
    def test_ordinary(self):
        interval = Interval(-1.5, 10)

        self.assertEqual(interval.get_formatted(), '(-1.5, 10)')

    def test_inclusive(self):
        interval = Interval(1, 3, is_end_inclusive=True)

        self.assertEqual(interval.get_formatted(), '(1, 3]')


class TestIntervalOverlap(unittest.TestCase):
    def test_negative(self):
        interval_1 = Interval(-1.5, 0.5)
        interval_2 = Interval(1, 3, is_end_inclusive=True)

        self.assertFalse(interval_1.is_overlapping(interval_2))
        self.assertFalse(interval_2.is_overlapping(interval_1))

    def test_positive(self):
        interval_1 = Interval(-1.5, 10)
        interval_2 = Interval(1, 3, is_end_inclusive=True)

        self.assertTrue(interval_1.is_overlapping(interval_2))
        self.assertTrue(interval_2.is_overlapping(interval_1))

    def test_negative_inclusive(self):
        interval_1 = Interval(-1.5, 1, is_end_inclusive=True)
        interval_2 = Interval(1, 3, is_end_inclusive=True)

        self.assertFalse(interval_1.is_overlapping(interval_2))
        self.assertFalse(interval_2.is_overlapping(interval_1))

    def test_positive_inclusive(self):
        interval_1 = Interval(-1.5, 1, is_end_inclusive=True)
        interval_2 = Interval(1, 3, is_start_inclusive=True)

        self.assertTrue(interval_1.is_overlapping(interval_2))
        self.assertTrue(interval_2.is_overlapping(interval_1))


class TestIntervalAlmostOverlap(unittest.TestCase):
    def test_ordinary_negative(self):
        interval_1 = Interval(-1.5, 0.5)
        interval_2 = Interval(1, 3, is_end_inclusive=True)

        self.assertFalse(interval_1.is_almost_overlapping(interval_2))
        self.assertFalse(interval_2.is_almost_overlapping(interval_1))

    def test_full_overlap(self):
        interval_1 = Interval(-1.5, 10)
        interval_2 = Interval(1, 3, is_end_inclusive=True)

        self.assertFalse(interval_1.is_almost_overlapping(interval_2))
        self.assertFalse(interval_2.is_almost_overlapping(interval_1))

    def test_negative_inclusive(self):
        interval_1 = Interval(-1.5, 1)
        interval_2 = Interval(1, 3, is_end_inclusive=True)

        self.assertFalse(interval_1.is_almost_overlapping(interval_2))
        self.assertFalse(interval_2.is_almost_overlapping(interval_1))

    def test_positive_inclusive(self):
        interval_1 = Interval(-1.5, 1, is_end_inclusive=True)
        interval_2 = Interval(1, 3)

        self.assertTrue(interval_1.is_almost_overlapping(interval_2))
        self.assertTrue(interval_2.is_almost_overlapping(interval_1))


class TestIntervalIncludes(unittest.TestCase):
    def test_inside(self):
        interval = Interval(1, 3)

        self.assertTrue(interval.includes(2.5))

    def test_start_negative(self):
        interval = Interval(1, 3)

        self.assertFalse(interval.includes(1))

    def test_start_positive(self):
        interval = Interval(1, 3, is_start_inclusive=True)

        self.assertTrue(interval.includes(1))

    def test_end_negative(self):
        interval = Interval(1, 3)

        self.assertFalse(interval.includes(3))

    def test_end_positive(self):
        interval = Interval(1, 3, is_end_inclusive=True)

        self.assertTrue(interval.includes(3))


class TestIntervalIntersection(unittest.TestCase):
    def test_ordinary(self):

        interval_1 = Interval(1, 3, is_end_inclusive=True)  # (1, 3]
        interval_2 = Interval(2, 5)  # (2, 5)

        intersection = Interval.intersection(interval_1, interval_2)  # (2, 3]

        self.assertEqual(intersection.start, 2)
        self.assertEqual(intersection.end, 3)
        self.assertFalse(intersection.is_start_inclusive)
        self.assertTrue(intersection.is_end_inclusive)

    def test_single_point(self):
        interval_1 = Interval(1, 3, is_start_inclusive=True)  # [1, 3)
        interval_2 = Interval(0, 1, is_end_inclusive=True)  # (0, 1]

        intersection = Interval.intersection(interval_1, interval_2)  # {1}

        self.assertEqual(intersection.start, 1)
        self.assertEqual(intersection.end, 1)
        self.assertTrue(intersection.is_start_inclusive)
        self.assertTrue(intersection.is_end_inclusive)

    def test_empty(self):
        interval_1 = Interval(1, 3, is_start_inclusive=True)  # [1, 3)
        interval_2 = Interval(0, 1)  # (0, 1)

        intersection = Interval.intersection(interval_1, interval_2)  # Empty

        self.assertEqual(intersection, None)


class TestIntervalUnion(unittest.TestCase):
    def test_overlapping(self):

        interval_1 = Interval(1, 3, is_end_inclusive=True)  # (1, 3]
        interval_2 = Interval(2, 5)  # (2, 5)

        union = Interval.union(interval_1, interval_2)  # (1, 5)

        self.assertEqual(len(union.intervals), 1)
        self.assertEqual(union.intervals[0].start, 1)
        self.assertEqual(union.intervals[0].end, 5)
        self.assertFalse(union.intervals[0].is_start_inclusive)
        self.assertFalse(union.intervals[0].is_end_inclusive)

    def test_almost_overlapping(self):
        interval_1 = Interval(1, 3, is_end_inclusive=True)  # (1, 3]
        interval_2 = Interval(0, 1, is_end_inclusive=True)  # (0, 1]

        union = Interval.union(interval_1, interval_2)  # (0, 3]

        self.assertEqual(len(union.intervals), 1)
        self.assertEqual(union.intervals[0].start, 0)
        self.assertEqual(union.intervals[0].end, 3)
        self.assertFalse(union.intervals[0].is_start_inclusive)
        self.assertTrue(union.intervals[0].is_end_inclusive)

    def test_separate(self):
        interval_1 = Interval(2, 3, is_start_inclusive=True)  # [2, 3)
        interval_2 = Interval(0, 1)  # (0, 1)

        union = Interval.union(interval_1, interval_2)  # Two intervals

        self.assertEqual(len(union.intervals), 2)


class TestNumericSetAdd(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
