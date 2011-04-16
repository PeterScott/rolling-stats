Rolling Statistics Library -- Work in progress
===================

A library for rolling statistics calculations over potentially very
long series of values.

Current classes
---------------

`MeanVariance`: Compute mean and variance for a series of
values. Works incrementally, in constant time and space. Add values to
the sample with `add(x)`, and use the `mean`, `sample_variance`, and
`population_variance` properties to get statistics.

`MovingAverage`: Compute an n-sample moving average. Initialize with
`MovingAverage(n)`, and add values with `add(x)`. Use the `mean`
property to get the moving average.

Testing
-------

Run the unit test suite with

    $ python tests.py
