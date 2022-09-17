import numpy as np
from Code.Learner import Learner


class GreedyLearner(Learner):
    def __init__(self, n_arms, n_products, customers, products_graph, prices, customers_distribution):
        super().__init__(n_arms, n_products, customers, products_graph, prices, customers_distribution)
        self.expected_rewards = [0] * n_products
        self.arms_selected = [0] * n_products  # start from all lowest price (0)
        product_available = [_ for _ in range(n_products)] #list with product tha can still increase their price
        self.new_configuration = np.zeros((n_products, n_products)).astype(int) #all new 5 configuration (arm) selected in this iteration
        self.best_reward = -1
        self.config_to_chose = 0
        self.products_available = []
        for config in range(n_products):
            self.products_available.append(product_available.copy())
        self.reword_config = [] #where I store the rewards of the 5 configurations
        self.report_config = []
        self.number_config = n_products #number of possible configuration equal the number of products since is an increment of one for each product
        self. counter = 0


    def select_superarm(self, rounds=None):
        """
        it should start from all lower prices, then pull one arm randomly each time (so increase its price)
        and evaluate it... each time increase just one until no improvement
        """
        if self.t!=0:
            if self.products_available[self.config_to_chose]:
                self.counter += 1
                product_random = np.random.choice(self.products_available[self.config_to_chose])
                self.new_configuration[self.config_to_chose, product_random] += 1
                if self.new_configuration[self.config_to_chose, product_random] == 3:
                    self.products_available[self.config_to_chose].remove(product_random)
                for c in range(self.number_config):
                    #remove the possible product from the other
                    if c != self.config_to_chose:
                        self.products_available[c].remove(product_random)
        return self.new_configuration[self.config_to_chose].copy()

    def update(self, pulled_arm, report):
        """""
        update the prior parameter accordingly to the arm pulled
        :param pulled_arm: list containing indexes of the arms in the super arm.
        :param report: real information about true data from environment
        :return:
        """
        if self.t == 0:
            self.update_observations(pulled_arm, report)
        else:
            #save the report of the new configuration
            prices = [self.prices[p][a] for p, a in enumerate(pulled_arm)]
            self.reword_config.append(report.reward(prices))
            self.report_config.append(report)
            self.update_observations(pulled_arm, report)
            if self.number_config == self.counter:
                #compare
                for c in range(self.number_config):
                    if self.best_reward < self.reword_config[c]:
                        config_selected = c
                        self.best_reward = self.reword_config[c]
                        self.arms_selected = self.new_configuration[c]
                self.config_to_chose = 0
                products_available = self.get_product_available(self.arms_selected)
                for config in range(self.number_config):
                    self.products_available[config] = products_available.copy()
                    self.new_configuration[config] = self.arms_selected.copy()
                self.reward_config = [] 
                self.report_config = []
                self.counter = 0
            else:
                self.config_to_chose += 1
        
        

    def get_product_available(self, arms_selected):
        sol = []
        number_of_maximum = 0
        for i in range(self.n_products):
            if arms_selected[i] < 3:
                sol.append(i)
            else:
                number_of_maximum += 1
        self.number_config = len(sol) #based on the number of products still available to be incremented (lower than maximum price)
        if self.number_config > 0:
            self.new_configuration = self.new_configuration[:self.number_config]
            self.products_available = self.products_available[:self.number_config]
        return sol


    def get_rewards(self):
        return self.history_rewards
