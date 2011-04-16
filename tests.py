# Tests for rolling stats library.

import stats
import unittest



class TestMeanVariance(unittest.TestCase):
    def test_pidigits(self):
        pidigits = "3141592653589793238462643383279502884197169"
        pidigits = [float(c) for c in pidigits]

        mv = stats.MeanVariance()
        for x in pidigits:
            mv.add(x)

        # Approximate tests, because there's inevitably some error.
        self.assertTrue(abs(mv.mean - 4.8837) < 0.0001)
        self.assertTrue(abs(mv.sample_variance - 7.67663344) < 0.0001)
        self.assertTrue(abs(mv.population_variance - 7.49810708) < 0.0001)


if __name__ == '__main__':
    unittest.main()
