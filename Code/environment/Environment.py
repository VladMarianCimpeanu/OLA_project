import numpy as np
import settings


class Environment:
    def __init__(self, n_arms, probabilities, customers_per_day):
        self.n_arms = n_arms
        self.probabilities = probabilities
        self.customers_per_day = customers_per_day
        self.customers_distribution = settings.customers_distribution  # categorical distribution

    def round(self, pulled_arm, customer=None) -> list:
        """
        simulate the customer and return for each product the conversion rate and the number of times
        it has been bought
        """
        pass

    def _generate_customer(self):
        pass
