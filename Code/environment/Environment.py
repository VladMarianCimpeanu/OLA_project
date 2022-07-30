import numpy as np
import settings


class Environment:
    def __init__(self, n_arms, probabilities, customers_per_day, p_lambda, products_graph):
        """
        :param n_arms:
        :param probabilities:
        :param customers_per_day:
        :param p_lambda: probability to observe second slot for secondary products
        :param products_graph: for each product this graph tells its secondary products and in which order.
        """
        # TODO: probabilities and arms embedded in behaviours file, I do not think there is any sense to pass these args
        self.n_arms = n_arms
        self.probabilities = probabilities
        self.customers_per_day = customers_per_day
        self.customers_distribution = settings.customers_distribution  # categorical distribution
        self.p_lambda = p_lambda

    def round(self, pulled_arm, customer=None) -> list:
        """
        simulate the customer and return for each product the conversion rate and the number of times
        it has been bought
        """
        pass

    def _generate_customer(self):
        pass

    @staticmethod
    def sample_categorical_distribution(probabilities):
        """
        implementation of categorical distribution sampler
        :param probabilities: array of probabilities for each item
        :return: index of the item sampled
        """
        assert sum(probabilities) == 1.0
        intervals = []
        for item in probabilities:
            upper_bound = item if len(intervals) == 0 else intervals[-1] + item
            intervals.append(upper_bound)
        print(intervals)
        assert intervals[-1] == 1.0
        uniform_sample = np.random.uniform(low=0, high=1)
        for index, item in enumerate(intervals):
            if uniform_sample <= item:
                return index
