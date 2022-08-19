import numpy as np
import sys
from math import ceil


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


def progress_bar(step, end):
    percentage = step / end * 100
    n_completed = ceil(percentage / 10)
    completed = "=" * n_completed
    to_complete = " " * (10 - n_completed)
    sys.stdout.write("\rloading: [{}{}] {}%".format(completed, to_complete, ceil(percentage)))


if __name__ == "__main__":
    import time

    for i in range(189):
        time.sleep(0.01)
        progress_bar(i, 189)
