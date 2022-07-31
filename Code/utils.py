import numpy as np


def sample_categorical_distribution(probabilities):
    """
    implementation of categorical distribution sampler
    :param probabilities: array of probabilities for each item
    :return: index of the item sampled
    """
    intervals = []
    for item in probabilities:
        upper_bound = item if len(intervals) == 0 else intervals[-1] + item
        intervals.append(upper_bound)
    uniform_sample = np.random.uniform(low=0, high=1)
    for index, item in enumerate(intervals):
        if uniform_sample <= item:
            return index
