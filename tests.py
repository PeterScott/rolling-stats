# Tests for rolling stats library.

import stats
import unittest

pidigits = "3141592653589793238462643383279502884197169"
pidigits = [float(c) for c in pidigits]
        

class TestMeanVariance(unittest.TestCase):
    def test_pidigits(self):
        mv = stats.MeanVariance()
        for x in pidigits:
            mv.add(x)

        # Approximate tests, because there's inevitably some error.
        self.assertTrue(abs(mv.mean - 4.8837) < 0.0001)
        self.assertTrue(abs(mv.sample_variance - 7.67663344) < 0.0001)
        self.assertTrue(abs(mv.population_variance - 7.49810708) < 0.0001)

class TestMovingAverage(unittest.TestCase):
    def test_pidigits(self):
        ma = stats.MovingAverage(5)

        for x in pidigits[:3]:
            ma.add(x)

        # Assert that when moving average object has received fewer
        # values than its window size, it just computes the average of
        # those values, and no dummy zeros.
        self.assertEqual(ma.mean, (3+1+4) / 3.0)

        for x in pidigits[3:]:
            ma.add(x)

        # Sum of last 5 digits in sequence
        self.assertEqual(ma.mean, 6.4000000000000004)

if __name__ == '__main__':
    unittest.main()
