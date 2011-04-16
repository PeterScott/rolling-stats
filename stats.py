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

class MovingAverage:
    """Compute an n-sample moving average. Before n samples are added,
    averages all samples that have been received yet."""
    
    def __init__(self, n):
        """Initialize, where n is the number of samples to average."""
        self.n = n                # Number of samples
        self.samples = [None] * n # Circular buffer
        self.i = 0                # Insertion index into buffer
        self.sum = 0.0            # Sum of values
        self.full = False         # Has the buffer been filled?

    def add(self, value):
        # Value leaving the set
        evicted = self.samples[self.i]
        if evicted is not None:
            self.sum -= evicted
        
        # Add new value to the circular buffer, update sum
        self.samples[self.i] = value
        self.i += 1
        if self.i == self.n:
            self.full = True
            self.i = 0
        self.sum += value

    @property
    def mean(self):
        if not self.full and self.i == 0:
            # Set is empty. FIXME: should this raise an exception?
            return 0.0

        if self.full:
            return self.sum / self.n
        else:
            return self.sum / self.i
