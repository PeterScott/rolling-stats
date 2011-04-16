"""Rolling statistics calculations, for potentially very long time series."""

import math

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
        self.size = 0             # Number of samples in window

    def add(self, x):
        """Add a value to the window, and return the element which was
        removed from the window (or None)."""
        evicted = self.samples[self.i]
        self.samples[self.i] = x
        self.i += 1
        if self.i == self.n:
            self.full = True
            self.i = 0
        
        # Update number of samples in window
        if self.full:
            self.size = self.n
        else:
            self.size = self.i

        return evicted


class MovingAverage:
    """Compute an n-sample moving average. Before n samples are added,
    averages all samples that have been received yet."""
    
    def __init__(self, n):
        """Initialize, where n is the number of samples to average."""
        self.window = SampleWindow(n)
        self.sum = 0.0
        self.size = 0

    def add(self, value):
        evicted = self.window.add(value)
        if evicted is not None:
            value -= evicted
        self.sum += value

    @property
    def mean(self):
        if self.window.size == 0:
            # Set is empty. FIXME: should this raise an exception?
            return 0.0
        return self.sum / self.window.size

# class MovingMeanVariance:
#     """Compute the n-sample moving mean and variance of a series of
#     values."""
# 
#     def __init__(self, n):
#         """Initialize, where n is the number of samples to average."""
#         self.window = SampleWindow(n)
#         self.sum = 0.0
#         self.M2 = 0.0
#         self.mean = 0.0
# 
#     def add(self, value):
#         # FIXME: the idea here is to maintain M2, a count of the sums
#         # of the squares of the differences from the current mean, and
#         # to update this with every value entering or leaving the
#         # window. But I messed up the math. I'll come back to this
#         # later.
#         evicted = self.window.add(value)
#         if evicted is not None:
#             self.sum -= evicted
#         self.sum += value
#         delta = value - self.mean
#         self.mean = self.sum / self.window.size
# 
#         if evicted is not None:
#             self.M2 -= (evicted - self.mean)**2
#         self.M2 += delta * (value - self.mean)
# 
#     @property
#     def sample_variance(self):
#         return self.M2 / (self.window.size - 1)
# 
#     @property
#     def population_variance(self):
#         return self.M2 / self.window.size


### Binned median calculation

class BinnedData:
    """Store a growing sample of data, where the values all can be
    sorted into some number of bins."""
    def __init__(self, min_value, max_value, nbins):
        """Initialize, for values in the interval [min_value,
        max_value), with a given number of bins. Note that min_value
        is an inclusive lower limit, but max_value is an exclusive
        upper limit."""
        self.min_value = float(min_value)
        self.max_value = float(max_value)
        self.bin_range = self.max_value - self.min_value
        self.nbins = nbins
        self.bins = [0.0] * nbins

    def add(self, value):
        """Add a value to the set."""
        if value < self.min_value or value >= self.max_value:
            raise ValueError, "Value %f out of bounds [%f, %f)" % \
                              (value, self.min_value, self.max_value)

        bin = int(math.floor((value - self.min_value) 
                             / self.bin_range * self.nbins))
        self.bins[bin] += 1


# class BinnedMedian:
#     """Calculate the median of a growing sample, where the values all
#     can be sorted into some number of bins. If the number of bins
#     equals the number of possible sample values -- if each possible
#     value gets a unique bin -- then this gives the exact
#     median. Otherwise, you can trade off memory versus precision by
#     changing the number of bins."""
# 
#     def __init__(self, min_value, max_value, nbins):
#         """Initialize, for values in the interval [min_value,
#         max_value), with a given number of bins. Note that min_value
#         is an inclusive lower limit, but max_value is an exclusive
#         upper limit."""
#         self.data = BinnedData(min_value, max_value, nbins)
#         
#     def add(self, value):
#         """Add a value to the set."""
#         self.data.add(value)
#         # FIXME: update median here.

            
