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
            #the index of the first probabilities higher than the uniform_sample
            return index


def superarm_to_int(s_arm):
    """
    map a super arm to an identifier integer
    :param s_arm: super arm to be casted
    :return: integer number
    """
    last = len(s_arm) - 1
    return sum([arm * 10 ** (last - index) for index, arm in enumerate(s_arm)])


def progress_bar(step, end, width=30):
    """
    print progress bar
    :param step: iteration of the process
    :param end: last iteration
    :return: None
    """
    percentage = step / end * 100
    n_completed = ceil(percentage / 100 * width)
    completed = "=" * n_completed
    to_complete = " " * (width - n_completed)
    sys.stdout.write("\rloading: [{}{}] {:0.1f}%".format(completed, to_complete, percentage))


if __name__ == "__main__":
    import time

    for t in range(189):
        time.sleep(0.01)
        progress_bar(t, 189, 50)

    print("\n", superarm_to_int([1, 4, 3, 2]))