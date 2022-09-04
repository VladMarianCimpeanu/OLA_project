from Code.Learner import Learner
import numpy as np


class NoisyClairvoyant(Learner):
    def __init__(self, n_arms, n_products, customers, products_graph, prices, customers_distribution, conversion_rates, std_noise=0.0):
        super().__init__(n_arms, n_products, customers, products_graph, prices, customers_distribution)
        self.conversion_rates = conversion_rates
        self.std_noise = std_noise

    def estimate_conversion_rates(self):
        return self.conversion_rates + np.random.normal(scale=self.std_noise, size=self.conversion_rates.shape)

    def update(self, pulled_arm, report):
        self.update_observations(pulled_arm, report)  # method of superclass
