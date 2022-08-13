import numpy as np
from Code.Learner import Learner

class GreedyLearner(Learner):
    def __init__(self, n_arms, n_products, customer, products_graph, arms):
        super().__init__(n_arms, n_products, customer, products_graph, arms)
        self.expected_rewards = [0]* n_products
        self.arms_selected = [0]* n_products #start from all lowest price (0)
        self.product_available = [_ for _ in range(n_products)]
        self.history_rewards = []
        self.best_reward = 0
        self.product_incremented = 0

    def select_superarm(self):
        "it should start from all lower prices, then pull one arm randomly each time (so increase its price) and evaluate it... each time increse just one until no improvement"
        if self.product_available:
            if self.t != 0:
                random_product = np.random.choice(self.product_available)
                self.arms_selected[random_product] += 1 
                self.product_incremented = random_product
                if self.arms_selected[random_product] == self.n_arms-1:
                #selected the highest price, remove this product from the possible choices
                    self.product_available.remove(random_product)
        return self.arms_selected

    def update(self, pulled_arm, report):
        """""
        update the prior parameter accordingly to the arm pulled
        :param pulled_arm:
        :param report: real information about true data from environment
        :return:
        """
        self.update_observations(pulled_arm, report)  #method of superclass
        num_bought = report.get_amount_bought()
        #update prior
        for i in range(self.n_products):
            self.expected_rewards[i] = pulled_arm[i]*num_bought[i]
        new_reward = sum(self.expected_rewards)
        if self.product_available:
            #already found the best solution only add reward in history
            if new_reward < self.best_reward and self.  product_incremented in self.product_available:
                self.product_available.remove(self.product_incremented)
                self.arms_selected[self.product_incremented] -= 1
            else:
                self.best_reward = new_reward
        self.history_rewards.append(new_reward)