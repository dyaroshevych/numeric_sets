"""Test Interval class methods from the 'numeric_sets' module using unittest."""


import unittest
from numeric_sets.main import Interval


class TestFormat(unittest.TestCase):
    def test_ordinary(self):
        interval = Interval(-1.5, 10)

        self.assertEqual(interval.get_formatted(), '(-1.5, 10)')

    def test_inclusive(self):
        interval = Interval(1, 3, is_end_inclusive=True)

        self.assertEqual(interval.get_formatted(), '(1, 3]')


class TestOverlap(unittest.TestCase):
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


class TestAlmostOverlap(unittest.TestCase):
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


class TestIncludes(unittest.TestCase):
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


class TestCopy(unittest.TestCase):
    def test_ordinary(self):
        interval = Interval(2, 3, is_end_inclusive=True)
        copy = interval.copy()

        self.assertEqual(interval.start, copy.start)
        self.assertEqual(interval.end, copy.end)
        self.assertEqual(interval.is_start_inclusive, copy.is_start_inclusive)
        self.assertEqual(interval.is_end_inclusive, copy.is_end_inclusive)


class TestDifference(unittest.TestCase):
    def test_unoverlapping(self):
        interval_1 = Interval(1, 3)  # (1, 3)
        interval_2 = Interval(4, 5)  # (4, 5)

        difference = Interval.difference(interval_1, interval_2)  # (1, 3)

        self.assertEqual(difference.start, 1)
        self.assertEqual(difference.end, 3)
        self.assertFalse(difference.is_start_inclusive)
        self.assertFalse(difference.is_end_inclusive)

    def test_left_overlap(self):
        interval_1 = Interval(1, 3)  # (1, 3)
        interval_2 = Interval(0, 2)  # (0, 2)

        difference = Interval.difference(interval_1, interval_2)  # [2, 3)

        self.assertEqual(len(difference.intervals), 1)
        self.assertEqual(difference.intervals[0].start, 2)
        self.assertEqual(difference.intervals[0].end, 3)
        self.assertTrue(difference.intervals[0].is_start_inclusive)
        self.assertFalse(difference.intervals[0].is_end_inclusive)

    def test_left_touch(self):
        interval_1 = Interval(1, 3, True, True)  # [1, 3]
        interval_2 = Interval(0, 1, is_end_inclusive=True)  # (0, 1]

        difference = Interval.difference(interval_1, interval_2)  # (1, 3]

        self.assertEqual(len(difference.intervals), 1)
        self.assertEqual(difference.intervals[0].start, 1)
        self.assertEqual(difference.intervals[0].end, 3)
        self.assertFalse(difference.intervals[0].is_start_inclusive)
        self.assertTrue(difference.intervals[0].is_end_inclusive)

    def test_right_overlap(self):
        interval_1 = Interval(0, 2)  # (0, 2)
        interval_2 = Interval(1, 3)  # (1, 3)

        difference = Interval.difference(interval_1, interval_2)  # (0, 1]

        self.assertEqual(len(difference.intervals), 1)
        self.assertEqual(difference.intervals[0].start, 0)
        self.assertEqual(difference.intervals[0].end, 1)
        self.assertFalse(difference.intervals[0].is_start_inclusive)
        self.assertTrue(difference.intervals[0].is_end_inclusive)

    def test_right_touch(self):
        interval_1 = Interval(0, 1, True, True)  # [0, 1]
        interval_2 = Interval(1, 3, is_start_inclusive=True)  # [1, 3)

        difference = Interval.difference(interval_1, interval_2)  # [0, 1)

        self.assertEqual(len(difference.intervals), 1)
        self.assertEqual(difference.intervals[0].start, 0)
        self.assertEqual(difference.intervals[0].end, 1)
        self.assertTrue(difference.intervals[0].is_start_inclusive)
        self.assertFalse(difference.intervals[0].is_end_inclusive)

    def test_split(self):
        interval_1 = Interval(0, 4, True, True)  # [0, 4]
        interval_2 = Interval(2, 3, is_start_inclusive=True)  # [2, 3)

        difference = Interval.difference(
            interval_1, interval_2)  # [0, 2) + [3, 4]

        self.assertEqual(len(difference.intervals), 2)

        self.assertEqual(difference.intervals[0].start, 0)
        self.assertEqual(difference.intervals[0].end, 2)
        self.assertTrue(difference.intervals[0].is_start_inclusive)
        self.assertFalse(difference.intervals[0].is_end_inclusive)

        self.assertEqual(difference.intervals[1].start, 3)
        self.assertEqual(difference.intervals[1].end, 4)
        self.assertTrue(difference.intervals[1].is_start_inclusive)
        self.assertTrue(difference.intervals[1].is_end_inclusive)


class TestIntersection(unittest.TestCase):
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


class TestUnion(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
