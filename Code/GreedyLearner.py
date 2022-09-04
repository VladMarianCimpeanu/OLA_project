import numpy as np
from Code.Learner import Learner


class GreedyLearner(Learner):
    def __init__(self, n_arms, n_products, customers, products_graph, prices, customers_distribution):
        super().__init__(n_arms, n_products, customers, products_graph, prices, customers_distribution)
        self.expected_rewards = [0] * n_products
        self.arms_selected = [0] * n_products  # start from all lowest price (0)
        self.product_available = [_ for _ in range(n_products)]
        self.best_reward = -1
        self.product_incremented = 0

    def select_superarm(self, rounds=None):
        """
        it should start from all lower prices, then pull one arm randomly each time (so increase its price)
        and evaluate it... each time increase just one until no improvement
        """
        previous_selected = self.arms_selected.copy()
        if self.product_available:
            if self.t != 0:
                random_product = np.random.choice(self.product_available)
                self.arms_selected[random_product] += 1
                self.product_incremented = random_product
        assert previous_selected != self.arms_selected or not self.product_available or self.t == 0
        return self.arms_selected.copy()

    def update(self, pulled_arm, report):
        """""
        update the prior parameter accordingly to the arm pulled
        :param pulled_arm: list containing indexes of the arms in the super arm.
        :param report: real information about true data from environment
        :return:
        """
        self.update_observations(pulled_arm, report)  # method of superclass
        new_reward = self.history_rewards[-1]
        if self.product_available:
            # already found the best solution only add reward in history
            if new_reward < self.best_reward:
                if self.product_incremented in self.product_available:
                    self.product_available.remove(self.product_incremented)
                self.arms_selected[self.product_incremented] -= 1
            else:
                self.best_reward = new_reward
            if self.arms_selected[self.product_incremented] == self.n_arms - 1:
                # selected the highest price, remove this product from the possible choices
                self.product_available.remove(self.product_incremented)

    def get_rewards(self):
        return self.history_rewards
