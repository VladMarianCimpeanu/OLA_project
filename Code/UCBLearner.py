import numpy as np
from Code.Learner import Learner


class UCBLearner(Learner):
    def __init__(self, n_arms, n_products, customers, products_graph, prices, customers_distribution):
        super().__init__(n_arms, n_products, customers, products_graph, prices, customers_distribution)
        self.means = np.zeros((n_products, n_arms))
        self.upper_bounds = np.full((n_products, n_arms), np.inf)
        self.seen = np.zeros((n_products, n_arms))

    def estimate_conversion_rates(self):
        return self.means + self.upper_bounds

    def update(self, pulled_arm, report):
        """
        update the confidence upper bounds of all arms and means of the pulled arms.
        :param pulled_arm: list containing indexes of the arms in the super arm.
        :param report: simulation report
        :return: None
        """
        self.update_observations(pulled_arm, report)  # method of superclass
        seen = np.array(report.get_seen())
        bought = np.array(report.get_bought())
        # update counter of samples seen
        tot_seen = np.copy(self.seen)
        for product, arm in enumerate(pulled_arm):
            tot_seen[product, arm] = tot_seen[product, arm] + seen[product]
        # update means
        for product, arm in enumerate(pulled_arm):
            if tot_seen[product, arm] > 0:
                self.means[product, arm] = (self.means[product, arm] * self.seen[product, arm] + bought[product]) / (tot_seen[product, arm])
        self.seen = tot_seen
        # update upper bounds
        for product in range(self.n_products):
            tot_samples = np.sum(self.seen[product])
            for arm in range(self.n_arms):
                if self.seen[product, arm] != 0:
                    self.upper_bounds[product, arm] = np.sqrt(2 * np.log(tot_samples) / self.seen[product, arm])