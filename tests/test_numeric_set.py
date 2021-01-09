"""Test NumericSet class methods from the 'NumericSets' module using unittest."""


import unittest
from numeric_sets.main import Interval, NumericSet


class TestAdd(unittest.TestCase):
    def test_regular(self):
        myset = NumericSet()
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
        myset = NumericSet()
        myset.add(Interval(2, 3))  # (2, 3)

        self.assertEqual(len(myset.intervals), 1)

    def test_start_overlapping_negative(self):
        myset = NumericSet()
        myset.add(Interval(2, 3))  # (2, 3)
        myset.add(Interval(1, 2))  # (1, 2)

        self.assertEqual(len(myset.intervals), 2)
        self.assertEqual(myset.intervals[0].get_formatted(), '(1, 2)')
        self.assertEqual(myset.intervals[1].get_formatted(), '(2, 3)')

    def test_start_overlapping_positive(self):
        myset = NumericSet()
        myset.add(Interval(2, 3))  # (2, 3)
        myset.add(Interval(1, 2, is_end_inclusive=True))  # (1, 2]

        self.assertEqual(len(myset.intervals), 1)
        self.assertEqual(myset.intervals[0].get_formatted(), '(1, 3)')

    def test_end_overlapping_negative(self):
        myset = NumericSet()
        myset.add(Interval(1, 2))  # (1, 2)
        myset.add(Interval(2, 3))  # (2, 3)

        self.assertEqual(len(myset.intervals), 2)
        self.assertEqual(myset.intervals[0].get_formatted(), '(1, 2)')
        self.assertEqual(myset.intervals[1].get_formatted(), '(2, 3)')

    def test_end_overlapping_positive(self):
        myset = NumericSet()
        myset.add(Interval(1, 2, is_end_inclusive=True))  # (1, 2]
        myset.add(Interval(2, 3))  # (2, 3)

        self.assertEqual(len(myset.intervals), 1)
        self.assertEqual(myset.intervals[0].get_formatted(), '(1, 3)')


class TestLeftIntervals(unittest.TestCase):
    def test_empty(self):
        myset = NumericSet()
        myset.add(Interval(1, 2))  # (1, 2)
        myset.add(Interval(2, 3))  # (2, 3)

        left_intervals = myset.get_left_intervals(Interval(0, 1.5))

        self.assertEqual(len(left_intervals), 0)

    def test_ordinary(self):
        myset = NumericSet()
        myset.add(Interval(1, 2))  # (1, 2)
        myset.add(Interval(2, 3))  # (2, 3)
        myset.add(Interval(4, 5))  # (4, 5)

        left_intervals = myset.get_left_intervals(Interval(3, 4))

        self.assertEqual(len(left_intervals), 2)


class TestRightIntervals(unittest.TestCase):
    def test_empty(self):
        myset = NumericSet()
        myset.add(Interval(1, 2))  # (1, 2)
        myset.add(Interval(2, 3))  # (2, 3)

        right_intervals = myset.get_right_intervals(Interval(1.5, 2.5))

        self.assertEqual(len(right_intervals), 0)

    def test_ordinary(self):
        myset = NumericSet()
        myset.add(Interval(1, 2))  # (1, 2)
        myset.add(Interval(2, 3))  # (2, 3)
        myset.add(Interval(4, 5))  # (4, 5)

        right_intervals = myset.get_right_intervals(Interval(3, 4))

        self.assertEqual(len(right_intervals), 1)


class TestClear(unittest.TestCase):
    def test_ordinary(self):
        myset = NumericSet()
        myset.add(Interval(1, 2))
        myset.add(Interval(2, 3))

        myset.clear()

        self.assertEqual(len(myset.intervals), 0)


class TestCopy(unittest.TestCase):
    def test_ordinary(self):
        myset = NumericSet()
        myset.add(Interval(1, 2))
        myset.add(Interval(2, 3))

        copy = myset.copy()

        self.assertEqual(copy.intervals[0].get_formatted(
        ), myset.intervals[0].get_formatted())
        self.assertEqual(copy.intervals[1].get_formatted(
        ), myset.intervals[1].get_formatted())


class TestDifference(unittest.TestCase):
    def test_ordinary(self):
        myset_1 = NumericSet()

        myset_1.add(Interval(2, 4))
        myset_1.add(Interval(5, 7))
        myset_1.add(Interval(8, 10))

        myset_2 = NumericSet()

        myset_2.add(Interval(3, 5))
        myset_2.add(Interval(6, 8))

        difference = myset_1.difference(myset_2)  # (2, 3] + (5, 6] + (8, 10)

        self.assertEqual(len(difference.intervals), 3)

        self.assertEqual(difference.intervals[0].start, 2)
        self.assertEqual(difference.intervals[0].end, 3)
        self.assertFalse(difference.intervals[0].is_start_inclusive)
        self.assertTrue(difference.intervals[0].is_end_inclusive)

        self.assertEqual(difference.intervals[1].start, 5)
        self.assertEqual(difference.intervals[1].end, 6)
        self.assertFalse(difference.intervals[1].is_start_inclusive)
        self.assertTrue(difference.intervals[1].is_end_inclusive)

        self.assertEqual(difference.intervals[2].start, 8)
        self.assertEqual(difference.intervals[2].end, 10)
        self.assertFalse(difference.intervals[2].is_start_inclusive)
        self.assertFalse(difference.intervals[2].is_end_inclusive)

    def test_points(self):
        myset_1 = NumericSet()

        myset_1.add(Interval(2, 4, True))
        myset_1.add(Interval(5, 7))
        myset_1.add(Interval(8, 10, is_end_inclusive=True))

        myset_2 = NumericSet()

        myset_2.add(Interval(2, 5))
        myset_2.add(Interval(5, 10))

        difference = myset_1.difference(myset_2)  # {2} + {10}

        self.assertEqual(len(difference.intervals), 2)

        self.assertEqual(difference.intervals[0].start, 2)
        self.assertEqual(difference.intervals[0].end, 2)
        self.assertTrue(difference.intervals[0].is_start_inclusive)
        self.assertTrue(difference.intervals[0].is_end_inclusive)

        self.assertEqual(difference.intervals[1].start, 10)
        self.assertEqual(difference.intervals[1].end, 10)
        self.assertTrue(difference.intervals[1].is_start_inclusive)
        self.assertTrue(difference.intervals[1].is_end_inclusive)


class TestIntersection(unittest.TestCase):
    def test_ordinary(self):
        myset_1 = NumericSet()

        myset_1.add(Interval(2, 4, is_end_inclusive=True))  # (2, 4]
        myset_1.add(Interval(5, 7))  # (5, 7)
        myset_1.add(Interval(8, 10, is_end_inclusive=True))  # (8, 10]

        myset_2 = NumericSet()

        myset_2.add(Interval(2, 5))  # (2, 5)
        myset_2.add(Interval(6, 9))  # (6, 9)

        intersection = myset_1.intersection(
            myset_2)  # (2, 4] + (6, 7) + (8, 9)

        self.assertEqual(len(intersection.intervals), 3)

        self.assertEqual(intersection.intervals[0].start, 2)
        self.assertEqual(intersection.intervals[0].end, 4)
        self.assertFalse(intersection.intervals[0].is_start_inclusive)
        self.assertTrue(intersection.intervals[0].is_end_inclusive)

        self.assertEqual(intersection.intervals[1].start, 6)
        self.assertEqual(intersection.intervals[1].end, 7)
        self.assertFalse(intersection.intervals[1].is_start_inclusive)
        self.assertFalse(intersection.intervals[1].is_end_inclusive)

        self.assertEqual(intersection.intervals[2].start, 8)
        self.assertEqual(intersection.intervals[2].end, 9)
        self.assertFalse(intersection.intervals[2].is_start_inclusive)
        self.assertFalse(intersection.intervals[2].is_end_inclusive)

    def test_points(self):
        myset_1 = NumericSet()

        myset_1.add(Interval(2, 4, is_end_inclusive=True))  # (2, 4]
        myset_1.add(Interval(5, 7, True))  # [5, 7)
        myset_1.add(Interval(8, 10, is_end_inclusive=True))  # (8, 10]

        myset_2 = NumericSet()

        myset_2.add(Interval(4, 5, True))  # [4, 5)
        myset_2.add(Interval(7, 8))  # (7, 8)

        intersection = myset_1.intersection(
            myset_2)  # {4}

        self.assertEqual(len(intersection.intervals), 1)

        self.assertEqual(intersection.intervals[0].start, 4)
        self.assertEqual(intersection.intervals[0].end, 4)
        self.assertTrue(intersection.intervals[0].is_start_inclusive)
        self.assertTrue(intersection.intervals[0].is_end_inclusive)


class TestSubset(unittest.TestCase):
    def test_ordinary_negative(self):
        myset_1 = NumericSet()

        myset_1.add(Interval(2, 4, is_end_inclusive=True))  # (2, 4]
        myset_1.add(Interval(5, 7, True))  # [5, 7)
        myset_1.add(Interval(8, 10, is_end_inclusive=True))  # (8, 10]

        myset_2 = NumericSet()

        myset_2.add(Interval(2, 10))  # (2, 10)

        self.assertFalse(myset_1.issubset(myset_2))
        self.assertFalse(myset_2.issubset(myset_1))

    def test_ordinary_positive(self):
        myset_1 = NumericSet()

        myset_1.add(Interval(2, 4, is_end_inclusive=True))  # (2, 4]
        myset_1.add(Interval(5, 7, True))  # [5, 7)
        myset_1.add(Interval(8, 10, is_end_inclusive=True))  # (8, 10]

        myset_2 = NumericSet()

        myset_2.add(Interval(2, 10, is_end_inclusive=True))  # (2, 10]

        self.assertTrue(myset_1.issubset(myset_2))
        self.assertFalse(myset_2.issubset(myset_1))


class TestSuperset(unittest.TestCase):
    def test_ordinary_negative(self):
        myset_1 = NumericSet()

        myset_1.add(Interval(2, 4, is_end_inclusive=True))  # (2, 4]
        myset_1.add(Interval(5, 7, True))  # [5, 7)
        myset_1.add(Interval(8, 10, is_end_inclusive=True))  # (8, 10]

        myset_2 = NumericSet()

        myset_2.add(Interval(2, 10))  # (2, 10)

        self.assertFalse(myset_1.issuperset(myset_2))
        self.assertFalse(myset_2.issuperset(myset_1))

    def test_ordinary_positive(self):
        myset_1 = NumericSet()

        myset_1.add(Interval(2, 4, is_end_inclusive=True))  # (2, 4]
        myset_1.add(Interval(5, 7, True))  # [5, 7)
        myset_1.add(Interval(8, 10, is_end_inclusive=True))  # (8, 10]

        myset_2 = NumericSet()

        myset_2.add(Interval(2, 10, is_end_inclusive=True))  # (2, 10]

        self.assertFalse(myset_1.issuperset(myset_2))
        self.assertTrue(myset_2.issuperset(myset_1))


class TestPop(unittest.TestCase):
    def test_ordinary(self):
        myset = NumericSet()
        interval = Interval(2, 4)

        myset.add(interval)

        self.assertEqual(myset.pop(), interval)

    def test_empty(self):
        myset = NumericSet()

        self.assertEqual(myset.pop(), None)


class TestRemove(unittest.TestCase):
    def test_points(self):
        myset = NumericSet()

        myset.add(Interval(2, 3, is_start_inclusive=True))
        myset.add(Interval(4, 5))
        myset.add(Interval(6, 7))
        myset.add(Interval(8, 9))
        myset.add(Interval(10, 11))
        myset.add(Interval(12, 13, is_end_inclusive=True))

        myset.remove(Interval(2, 13))

        self.assertEqual(len(myset.intervals), 2)

        self.assertEqual(myset.intervals[0].start, 2)
        self.assertEqual(myset.intervals[0].end, 2)
        self.assertTrue(myset.intervals[0].is_start_inclusive)
        self.assertTrue(myset.intervals[0].is_end_inclusive)

        self.assertEqual(myset.intervals[1].start, 13)
        self.assertEqual(myset.intervals[1].end, 13)
        self.assertTrue(myset.intervals[1].is_start_inclusive)
        self.assertTrue(myset.intervals[1].is_end_inclusive)

    def test_ordinary(self):
        myset = NumericSet()

        myset.add(Interval(2, 3))
        myset.add(Interval(4, 5))
        myset.add(Interval(6, 7))
        myset.add(Interval(8, 9))
        myset.add(Interval(10, 11))
        myset.add(Interval(12, 13))

        myset.remove(Interval(2.5, 12.5))

        self.assertEqual(len(myset.intervals), 2)

        self.assertEqual(myset.intervals[0].start, 2)
        self.assertEqual(myset.intervals[0].end, 2.5)
        self.assertFalse(myset.intervals[0].is_start_inclusive)
        self.assertTrue(myset.intervals[0].is_end_inclusive)

        self.assertEqual(myset.intervals[1].start, 12.5)
        self.assertEqual(myset.intervals[1].end, 13)
        self.assertTrue(myset.intervals[1].is_start_inclusive)
        self.assertFalse(myset.intervals[1].is_end_inclusive)


class TestSymmetricDifference(unittest.TestCase):
    def test_ordinary(self):
        myset_1 = NumericSet()

        myset_1.add(Interval(2, 4, True, True))  # [2, 4]
        myset_1.add(Interval(5, 7))  # (5, 7)
        myset_1.add(Interval(8, 10, is_end_inclusive=True))  # (8, 10]

        myset_2 = NumericSet()

        myset_2.add(Interval(2, 5))  # (2, 5)
        myset_2.add(Interval(6, 9))  # (6, 9)

        symmetric_diff = myset_1.symmetric_difference(
            myset_2)  # {2} + (4, 5) + [7, 8] + [9, 10]

        self.assertEqual(len(symmetric_diff.intervals), 5)

        self.assertEqual(symmetric_diff.intervals[0].start, 2)
        self.assertEqual(symmetric_diff.intervals[0].end, 2)
        self.assertTrue(symmetric_diff.intervals[0].is_start_inclusive)
        self.assertTrue(symmetric_diff.intervals[0].is_end_inclusive)

        self.assertEqual(symmetric_diff.intervals[1].start, 4)
        self.assertEqual(symmetric_diff.intervals[1].end, 5)
        self.assertFalse(symmetric_diff.intervals[1].is_start_inclusive)
        self.assertFalse(symmetric_diff.intervals[1].is_end_inclusive)

        self.assertEqual(symmetric_diff.intervals[2].start, 5)
        self.assertEqual(symmetric_diff.intervals[2].end, 6)
        self.assertFalse(symmetric_diff.intervals[2].is_start_inclusive)
        self.assertTrue(symmetric_diff.intervals[2].is_end_inclusive)

        self.assertEqual(symmetric_diff.intervals[3].start, 7)
        self.assertEqual(symmetric_diff.intervals[3].end, 8)
        self.assertTrue(symmetric_diff.intervals[3].is_start_inclusive)
        self.assertTrue(symmetric_diff.intervals[3].is_end_inclusive)

        self.assertEqual(symmetric_diff.intervals[4].start, 9)
        self.assertEqual(symmetric_diff.intervals[4].end, 10)
        self.assertTrue(symmetric_diff.intervals[4].is_start_inclusive)
        self.assertTrue(symmetric_diff.intervals[4].is_end_inclusive)


class TestUnion(unittest.TestCase):
    def test_ordinary(self):
        myset_1 = NumericSet()

        myset_1.add(Interval(2, 4, True, True))  # [2, 4]
        myset_1.add(Interval(5, 7))  # (5, 7)
        myset_1.add(Interval(8, 10, is_end_inclusive=True))  # (8, 10]

        myset_2 = NumericSet()

        myset_2.add(Interval(2, 5))  # (2, 5)
        myset_2.add(Interval(6, 9))  # (6, 9)

        union = myset_1.union(
            myset_2)  # [2, 5) + (5, 10]

        self.assertEqual(len(union.intervals), 2)

        self.assertEqual(union.intervals[0].start, 2)
        self.assertEqual(union.intervals[0].end, 5)
        self.assertTrue(union.intervals[0].is_start_inclusive)
        self.assertFalse(union.intervals[0].is_end_inclusive)

        self.assertEqual(union.intervals[1].start, 5)
        self.assertEqual(union.intervals[1].end, 10)
        self.assertFalse(union.intervals[1].is_start_inclusive)
        self.assertTrue(union.intervals[1].is_end_inclusive)


class TestEmpty(unittest.TestCase):
    def test_ordinary_negative(self):
        myset = NumericSet()

        self.assertTrue(myset.is_empty())

    def test_ordinary_positive(self):
        myset = NumericSet()
        myset.add(Interval(2, 4))

        self.assertFalse(myset.is_empty())


if __name__ == '__main__':
    unittest.main()
