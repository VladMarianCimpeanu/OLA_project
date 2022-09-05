import numpy as np
from Code.MC_simulator import Simulator
import json
import os
from Code.environment.settings import customers_distribution
from Code.environment.Customer import Customer
import copy
from multiprocessing import Pool


def evaluate_superarm(params):
    simulation, prices, super_arm = params
    prices = [prices[p][a] for p, a in enumerate(super_arm)]
    return sum([price * num for price, num in zip(prices, simulation.run_dp(super_arm))])


class Learner:
    def __init__(self, n_arms, n_products, customers, products_graph, prices, customers_distribution):
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
        self.customers = copy.deepcopy(customers)
        self.customers_distribution = copy.deepcopy(customers_distribution)
        self.prices = copy.deepcopy(prices)
        self.pulled = []
        self.t = 0
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
        self.__init__(self.n_arms, self.n_products, self.customers, self.products_graph, self.arms,
                      self.customers_distribution)

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

    def select_superarm(self, rounds=100, reward=False):
        """
        This method runs a montecarlo simulation for each combination of arms in order to determine the best superarm.
        :param rounds: number of simulations that must be run for each combinations of arms
        :return: a list containing the indexes of the best arms for each product according to the MC simulation.
        """

        conversion_rates = self.estimate_conversion_rates()
        conversion_rates = np.clip(conversion_rates, 0, 1)
        for customer in self.customers:
            customer.set_probability_buy(conversion_rates)
        simulation = Simulator(self.customers, self.graph, self.customers_distribution)

        with Pool(processes=8) as pool:
            rewards = pool.imap(evaluate_superarm, [(simulation, self.prices, arm) for arm in self.super_arms])
            # rewards = [evaluate_superarm((simulation, self.prices, arm)) for arm in self.super_arms]
            # print(rewards, self.super_arms)
            maximum_estimate, best_super_arm = max(zip(rewards, self.super_arms))

        if reward:
            return best_super_arm, maximum_estimate
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
