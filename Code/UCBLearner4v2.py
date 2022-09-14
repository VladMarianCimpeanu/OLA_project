import numpy as np
from Code.Learner import Learner
from Code.UCBLearner import UCBLearner


class UCBLearner4(UCBLearner):
    def __init__(self, n_arms, n_products, customers, products_graph, prices, customers_distribution, debug=False):
        super().__init__(n_arms, n_products, customers, products_graph, prices, customers_distribution)
        self.estimated_alphas = np.zeros(n_products)
        self.estimated_n_items = np.zeros((n_products, n_arms))
        self.estimated_n_bought = np.zeros((n_products, n_arms))
        self.mean_items = np.zeros((n_products, n_arms))
        self.upper_bounds_items = np.full((n_products, n_arms), np.inf)

        self.debug = debug

    def update(self, pulled_arm, report):
        if self.debug:
            print("customer alpha:", self.customers[0].get_distribution_alpha())
        super().update(pulled_arm, report)
        self.estimated_alphas = self.estimated_alphas + np.array(report.get_starts())
        for customer in self.customers:
            customer.set_distribution_alpha(self.estimated_alphas / sum(self.estimated_alphas))


        # update means of num_prod
        seen = self.estimated_n_items.copy()  # old quantity
        bought = report.get_amount_bought()
        for p, a in enumerate(pulled_arm):
            self.estimated_n_items[p, a] += report.get_bought()[p]  # number of times customer decides to buy
            self.estimated_n_bought[p, a] += report.get_amount_bought()[p]  # quantity

            if self.estimated_n_items[p, a] > 0:
                self.mean_items[p, a] = (self.mean_items[p, a] * seen[p, a] + bought[p]) / (
                self.estimated_n_items[p, a])

        # update upper bounds for num_prod
        for product in range(self.n_products):
            tot_samples = np.sum(self.estimated_n_items[product])
            for arm in range(self.n_arms):
                if self.estimated_n_items[product, arm] != 0:
                    self.upper_bounds_items[product, arm] = np.sqrt(2 * np.log(tot_samples) / self.estimated_n_items[product, arm])

        #new_mean = 1 / np.maximum(self.mean_items.copy(), 1e-4)

        #for customer in self.customers:
            #customer.set_num_prods(new_mean)


    def select_superarm(self, rounds=100, reward=False):
        # set new value of n_prod
        new_val = self.mean_items.copy() / 20 + self.upper_bounds_items.copy()
        inverse_mean = np.minimum(1 / np.maximum(new_val * 20, 1e-4), 1e4)

        for customer in self.customers:
            customer.set_num_prods(inverse_mean)
        return super().select_superarm()


