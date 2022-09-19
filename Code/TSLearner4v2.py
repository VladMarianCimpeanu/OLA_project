import numpy as np
from Code.Learner import Learner
from Code.TSLearner import TSLearner


class TSLearner4(TSLearner):
    def __init__(self, n_arms, n_products, customers, products_graph, prices, customers_distribution):
        super().__init__(n_arms, n_products, customers, products_graph, prices, customers_distribution)
        self.estimated_alphas = np.zeros(n_products)
        self.beta_items_parameters = np.ones((n_products, n_arms, 2))

    def update(self, pulled_arm, report):
        """
        Override of the update method of TSLearner class
        here this class also estimates the alpha ratios and the number of items sold per product
        """
        super().update(pulled_arm, report)
        self.estimated_alphas = self.estimated_alphas + np.array(report.get_starts())
        for customer in self.customers:
            customer.set_distribution_alpha(self.estimated_alphas / sum(self.estimated_alphas))

        # update beta parameters for n_prod
        tot_bought = report.get_amount_bought()
        seen = report.get_bought()
        for index, arm in enumerate(pulled_arm):
            self.beta_items_parameters[index, arm, 0] = self.beta_items_parameters[index, arm, 0] + seen[index]
            self.beta_items_parameters[index, arm, 1] = self.beta_items_parameters[index, arm, 1] + tot_bought[index]

    def select_superarm(self, rounds=100, reward=False):
        # set new value of n_prod
        for customer in self.customers:
            customer.set_num_prods(np.random.beta(a=self.beta_items_parameters[:, :, 0], b=self.beta_items_parameters[:, :, 1]))
        return super().select_superarm()

