"""Rolling statistics calculations, for potentially very long time series."""

class MeanVariance:
    """Compute mean and variance for a series of values. The series of
    values can only be added to."""

    # Uses one-pass algorithm described in
    # http://en.wikipedia.org/wiki/Algorithms_for_calculating_variance

    def __init__(self):
        # Values updated on every step
        self.n = 0
        self.mean = 0
        self.M2 = 0

    def add(self, value):
        """Add a value to the sample."""
        value = float(value)    # Ensure floating point arithmetic
        self.n += 1
        delta = value - self.mean
        self.mean += delta / self.n
        self.M2 += delta * (value - self.mean)

    @property
    def sample_variance(self):
        return self.M2 / (self.n - 1)

    @property
    def population_variance(self):
        return self.M2 / self.n
