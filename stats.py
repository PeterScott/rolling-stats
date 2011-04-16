"""Rolling statistics calculations, for potentially very long time series."""

### Statistics for a sample that can only be added to.

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


### Windowed statistics -- only consider last n samples.

class SampleWindow:
    """Helper class for holding a window of n samples."""
    
    def __init__(self, n):
        """Initialize, where n is the number of samples in the
        window."""
        self.n = n                # Number of samples
        self.samples = [None] * n # Circular buffer
        self.i = 0                # Insertion index into buffer
        self.full = False         # Has the buffer been filled?

    def add(self, x):
        """Add a value to the window, and return (evicted, size) where
        `evicted` is the element which was removed from the window (or
        None), and `size` is the current number of samples in the
        window, which may be less than n if the window has not yet
        been filled up."""
        evicted = self.samples[self.i]
        self.samples[self.i] = x
        self.i += 1
        if self.i == self.n:
            self.full = True
            self.i = 0
        
        if self.full:
            size = self.n
        else:
            size = self.i

        return evicted, size


class MovingAverage:
    """Compute an n-sample moving average. Before n samples are added,
    averages all samples that have been received yet."""
    
    def __init__(self, n):
        """Initialize, where n is the number of samples to average."""
        self.window = SampleWindow(n)
        self.sum = 0.0
        self.size = 0

    def add(self, value):
        evicted, size = self.window.add(value)
        if evicted is not None:
            value -= evicted
        self.sum += value
        self.size = size

    @property
    def mean(self):
        if self.size == 0:
            # Set is empty. FIXME: should this raise an exception?
            return 0.0
        return self.sum / self.size

