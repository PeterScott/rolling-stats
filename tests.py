# Tests for rolling stats library.

import simplestats
import stats
import unittest
import random

pidigits = "3141592653589793238462643383279502884197169"
pidigits = [float(c) for c in pidigits]


class TestSampleWindow(unittest.TestCase):
    def test_window(self):
        window = stats.SampleWindow(10)
        for i in range(100):
            evicted = window.add(i)
            size = window.size
            if i < 10:
                self.assertEqual(i + 1, size)
                self.assertEqual(None, evicted)
            else:
                self.assertEqual(10, size)
                self.assertEqual(i - 10, evicted)


class TestMeanVariance(unittest.TestCase):
    def test_pidigits(self):
        mv = stats.MeanVariance()
        for x in pidigits:
            mv.add(x)

        # Approximate tests, because there's inevitably some error.
        self.assertAlmostEqual(4.88372093, mv.mean)
        self.assertAlmostEqual(7.67663344, mv.sample_variance)
        self.assertAlmostEqual(7.49810708, mv.population_variance)


class TestMovingAverage(unittest.TestCase):
    def test_pidigits(self):
        ma = stats.MovingAverage(5)

        for x in pidigits[:3]:
            ma.add(x)

        # Assert that when moving average object has received fewer
        # values than its window size, it just computes the average of
        # those values, and no dummy zeros.
        self.assertAlmostEqual(ma.mean, (3+1+4) / 3.0)

        for x in pidigits[3:]:
            ma.add(x)

        # Sum of last 5 digits in sequence
        self.assertAlmostEqual(6.4, ma.mean)
        
        
# class TestMovingMeanVariance(unittest.TestCase):
#     def test_pidigits(self):
#         mmv = stats.MovingMeanVariance(5)
#         
#         for i, x in enumerate(pidigits[1:]):
#             mmv.add(x)
#             # Don't assert with only one value because sample variance returns a division by zero at that point.
#             if i:
#                 expected_sample_variance, expected_population_variance = simplestats.variance(pidigits[max(0, i - 4):i+1])
#                 self.assertAlmostEqual(
#                     expected_sample_variance, mmv.sample_variance,
#                     msg="Sample variance failed at index %d: %f != %f" % (
#                         i, expected_sample_variance, mmv.sample_variance))
#                 self.assertAlmostEqual(
#                     expected_sample_variance, mmv.sample_variance,
#                     msg="Population variance failed at index %d: %f != %f" % (
#                         i, expected_sample_variance, mmv.sample_variance))
        

class TestBinnedMedian(unittest.TestCase):
    def test_uniform(self):
        # Insert uniformly distributed random values with known seed.
        random.seed(123456)
        bm = stats.BinnedMedian(5, 10, 10000)
        for i in range(100000):
            bm.add(random.uniform(5, 9.99999999))
        self.assertAlmostEqual(bm.median, 7.50325)

        # Now a smaller number of values
        random.seed(123456)
        bm = stats.BinnedMedian(5, 10, 10000)
        for i in range(10):
            bm.add(random.uniform(5, 9.99999999))
        self.assertAlmostEqual(bm.median, 5.87325)

        # Finally, fewer bins
        random.seed(123456)
        bm = stats.BinnedMedian(5, 10, 10)
        for i in range(10000):
            bm.add(random.uniform(5, 9.99999999))
        self.assertAlmostEqual(bm.median, 5.75)

class TestExactBinnedMedian(unittest.TestCase):
    def test_pidigits(self):
        eb = stats.ExactBinnedMedian(0, 9)
        for x in pidigits:
            eb.add(x)
        self.assertEqual(eb.median, simplestats.median(pidigits))

if __name__ == '__main__':
    unittest.main()
