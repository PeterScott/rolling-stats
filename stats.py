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
        self.size = 0

    def add(self, value):
        """Add a value to the set."""
        bin = self.bin(value)
        self.bins[bin] += 1
        self.size += 1

    def bin(self, value):
        """Return the bin index of a given value. Throws ValueError if
        the value is out of range."""
        if value < self.min_value or value >= self.max_value:
            raise ValueError, "Value %f out of bounds [%f, %f)" % \
                              (value, self.min_value, self.max_value)

        return int(math.floor((value - self.min_value) 
                              / self.bin_range * self.nbins))

    def unbin(self, bin):
        """Return the average value that would be sorted into the
        given bin, assuming uniform distribution."""
        bin_start = (bin / float(self.nbins) * self.bin_range) + self.min_value
        bin_width = self.bin_range / self.nbins
        return bin_start + bin_width / 2.0

class BinnedMedian:
    """Calculate the median of a growing sample, where the values all
    can be sorted into some number of bins. If the number of bins
    equals the number of possible sample values -- if each possible
    value gets a unique bin -- then this gives the exact
    median. Otherwise, you can trade off memory versus precision by
    changing the number of bins."""

    def __init__(self, min_value, max_value, nbins):
        """Initialize, for values in the interval [min_value,
        max_value), with a given number of bins. Note that min_value
        is an inclusive lower limit, but max_value is an exclusive
        upper limit."""
        self.data = BinnedData(min_value, max_value, nbins)
        # Track median and which bin has the median.
        self.median = None
        self.median_bin = 0
        self.median_offset = 0
        # Number of elements before and after the median
        self.before_median = 0
        self.after_median  = 0
        # Equal values are put either before or after the median, in
        # an alternating fashion. This variable controls that.
        self.flipflop = False
        
    def add(self, value):
        """Add a value to the set."""
        self.data.add(value)
        bin = self.data.bin(value)

        if self.median is None:
            # Only one element; it becomes the median.
            self.median = value
            self.median_bin = bin
        else:
            # Update before/after median element counts
            if bin < self.median_bin:
                self.before_median += 1
            elif bin > self.median_bin:
                self.after_median += 1
            else:
                if self.flipflop:
                    self.before_median += 1
                    self.flipflop = False
                else:                    
                    self.after_median += 1
                    self.flipflop = True

            # Move median if necessary
            if self.before_median - self.after_median == 2:
                self.before_median -= 1
                self.after_median += 1
                if self.median_offset == 0:
                    # Go left to first non-empty bin.
                    self.median_bin -= 1
                    while self.data.bins[self.median_bin] == 0:
                        self.median_bin -= 1
                    self.median_offset = self.data.bins[self.median_bin] - 1
                self.median = self.data.unbin(self.median_bin)
            elif self.after_median - self.before_median == 2:
                self.before_median += 1
                self.after_median -= 1
                if self.median_offset == 0:
                    # Go right to first non-empty bin.
                    self.median_bin += 1
                    while self.data.bins[self.median_bin] == 0:
                        self.median_bin += 1
                    self.median_offset = 0
                self.median = self.data.unbin(self.median_bin)
