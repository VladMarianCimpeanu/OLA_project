import numpy as np
from Code.MC_simulator import Simulator
import json
import os
from Code.environment.Customer import Customer
import copy


class Learner:
    def __init__(self, n_arms, n_products, customer, products_graph, prices):
        """
        :param n_arms: number of arms
        :param n_products: number of products
        :param customer: customer contains all the BELIVED information about the customer by the learner.
        The learner updates the customer's attributes that are not known. The base class assumes that only the conversion
        rate should be estimated, so no customer's attribute will be updated apart from the conversion rates.
        :param products_graph: name of the json file in Code/data with all the relevant information
        about the products graph given by the business unit. The file must contain a key named 'graph', whereas its
        value is the graph in matrix form.
        :param prices: arms of the learner. Matrix whose rows are the products whereas the columns are the prices
        """
        self.n_arms = n_arms
        self.n_products = n_products
        self.t = 0
        self.customer = Customer(0, 0)
        self.pulled = []
        self.prices = prices
        # load products graph
        self.products_graph = products_graph
        self.graph = self._load_products(products_graph)
        self.super_arms = self._get_enumerations()
        self.history_rewards = []
        self.history_expected = []

    @classmethod
    def _load_products(cls, name):
        file_position = "{}/data/{}".format(os.path.dirname(os.path.abspath(__file__)), name)
        file = open(file_position)
        data = json.load(file)
        return data['graph']

    def reset(self):
        """
        reset the learner to the initial state.
        :return: None
        """
        self.__init__(self.n_arms, self.n_products, self.customer, self.products_graph, self.arms)

    def update_observations(self, pulled_arm, report):
        """
        :param pulled_arm: list containing indexes of the pulled arms.
        :param report: simulation report
        :return: None
        """
        self.t += 1
        prices = [self.prices[p][a] for p, a in enumerate(pulled_arm)]
        self.history_rewards.append(report.reward(prices))
        self.history_expected.append(report.expected_reward(prices))
        self.pulled.append(pulled_arm.copy())

    def select_superarm(self, rounds=50):
        """
        This method runs a montecarlo simulation for each combination of arms in order to determine the best superarm.
        :param rounds: number of simulations that must be run for each combinations of arms
        :return: a list containing the indexes of the best arms for each product according to the MC simulation.
        """
        conversion_rates = self.estimate_conversion_rates()
        conversion_rates = np.clip(conversion_rates, 0, 1)
        self.customer.set_probability_buy(conversion_rates)
        simulation = Simulator([self.customer], self.graph, [1])
        maximum_estimate = -1  # assuming that a reward is a non-negative number.
        best_super_arm = None
        for super_arm in self.super_arms:
            prices = [self.prices[p][a] for p, a in enumerate(super_arm)]
            reward = rounds * sum([price*num for price, num in zip(prices, simulation.run_dp(super_arm))])
            if reward > maximum_estimate:
                maximum_estimate = reward
                best_super_arm = super_arm
        return best_super_arm

    def _get_enumerations(self, depth=0, indexes=None, combinations=None):
        """
        brute force method to enumerate all the possible combinations of arms
        :param depth: current depth in the search tree. By default it is set to 0 (root of the search tree)
        :param indexes: list containing the indexes belonging to a single combination. Keep it None.
        :param combinations: list containing all the combinations found. Keep it None
        :return: a list containing all the possible combinations.
        """
        if indexes is None:
            indexes = []
        if combinations is None:
            combinations = []
        if depth == self.n_products:
            combinations.append(indexes)
            return combinations
        new_depth = depth + 1
        for element in range(self.n_arms):
            new_indexes = indexes.copy()
            new_indexes.append(element)
            combinations = self._get_enumerations(new_depth, new_indexes, combinations)
        return combinations

    def estimate_conversion_rates(self):
        """
        This method evaluate the conversion rate associated to each arm based on the specific algorithm has been used.
        This method should be overridden by each subclass of Learner.
        :return: matrix whose rows are products and columns are conversion rates associated to a specific arm (price).
        """
        return np.array([])

    def get_all_pulled(self):
        """
        Return all the pulled arms by the learner.
        :return: a list whose elements are super arms pulled by the learner. A super arm is a list and its i-th element
        is the index of the arm pulled for the i-th product.
        """
        return self.pulled

    def get_last_pulled(self):
        """
        Return the last super arm pulled by the learner.
        :return:  A super arm is a list and its i-th element
        is the index of the arm pulled for the i-th product.
        """
        return self.pulled[-1]

    def get_expected_rewards(self):
        """
        Return the average reward per day
        :return: a list whose elements are the reward average for a specific day.
        """
        return self.history_expected

    def get_daily_rewards(self):
        """
        Return the rewards per day
        :return: a list containing the cumulative reward per day
        """
        return self.history_rewards
