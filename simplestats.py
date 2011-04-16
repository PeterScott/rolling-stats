### Simple O(n) sample statistics, for debugging

def mean(sample):
    """Compute the mean of a sample, where `sample` is a list."""
    return float(sum(sample)) / float(len(sample))

def variance(sample):
    """Compute the sample and population variance of a list of
    numbers. May not be numerically stable for very large lists; in
    that case, use `MeanVariance` instead."""
    avg = mean(sample)

    sumsquares = 0.0
    for x in sample:
        delta = x - avg
        sumsquares += delta * delta
    
    return (sumsquares / (len(sample) - 1), sumsquares / len(sample))
