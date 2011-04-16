Rolling Statistics Library
===================

A library for rolling statistics calculations over potentially very
long series of values. It's still pretty rough. All the classes for
computing rolling statistics perform all their operations in constant
time, making them useful for dealing with very large streams of data.

Demo
----

This will take some numbers and compute their mean and variance:

    >>> import stats
    >>> mv = stats.MeanVariance()
    >>> for x in [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 7]:
    ...     mv.add(x)
    ... 
    >>> mv.mean
    4.5384615384615383
    >>> mv.sample_variance
    6.435897435897437
    >>> mv.population_variance
    5.9408284023668649

Note that `MeanVariance` does not store the numbers themselves, so the
amount of memory it uses stays constant no matter how many numbers are
added.

There are other classes for computing an n-sample moving average, and
medians of integers or binned real numbers within a given range; see
below for details.

Current classes
---------------

`MeanVariance`: Compute mean and variance for a series of
values. Works incrementally, in constant time and space. Add values to
the sample with `add(x)`, and use the `mean`, `sample_variance`, and
`population_variance` properties to get statistics.

`MovingAverage`: Compute an n-sample moving average. Initialize with
`MovingAverage(n)`, and add values with `add(x)`. Use the `mean`
property to get the moving average.

`BinnedMedian`: Takes values within a predefined range and sorts them
into a number of bins. Computes the median value of this discretized
stream of samples. You can trade off space versus accuracy by
increasing or decreasing the number of bins.

`ExactBinnedMedian`: Like BinnedMedian, where the values are integers
in a predefined range. Allocates exactly enough bins to hold all the
values, so the median you get will be accurate.

There are also some functions in `simplestats.py` that you can use for
really simple O(n) calculations of mean, variance, and median.

Testing
-------

Run the unit test suite with

    $ python tests.py
