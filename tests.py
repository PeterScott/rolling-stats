# Tests for rolling stats library.

import stats
import unittest

pidigits = "3141592653589793238462643383279502884197169"
pidigits = [float(c) for c in pidigits]


class TestSampleWindow(unittest.TestCase):
    def test_window(self):
        window = stats.SampleWindow(10)
        for i in range(100):
            evicted, size = window.add(i)
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


if __name__ == '__main__':
    unittest.main()
