import numpy as np
from MC_simulator import Simulator
import json


class Learner:
    def __init__(self, n_arms, n_products, customer, products_graph, arms):
        """
        :param n_arms: number of arms
        :param n_products: number of products
        :param customer: customer contains all the BELIVED information about the customer by the learner.
        The learner updates the customer's attributes that are not known. The base class assumes that only the conversion
        rate should be estimated, so no customer's attribute will be updated.
        :param products_graph: name of the json file in Code/data with all the relevant information
        about the products graph given by the business unit. The file must contain a key named 'graph', whereas its
        value is the graph in matrix form.
        :param arms: arms of the learner. Matrix whose rows are the products whereas the columns are the prices
        """
        self.n_arms = n_arms
        self.arms = arms
        self.n_products = n_products
        self.t = 0
        self.rewards_per_arm = np.array([
            [
                0 for j in range(n_arms)
            ] for i in range(n_products)
        ])
        self.collected_rewards = np.array([
            [
                [] for j in range(n_arms)
            ] for i in range(n_products)
        ])
        self.customer = customer
        # load products graph
        self.graph = self._load_products(products_graph)
        self.super_arms = self._get_enumerations()

    @classmethod
    def _load_products(cls, name):
        file = open('Code/data/{}'.format(name))
        data = json.load(file)
        return data['graph']

    def reset(self):
        self.__init__(self.n_arms, self.t)

    def update(self, pulled_arm, report):
        pass

    def select_superarm(self, rounds=10):
        """
        This method runs a montecarlo simulation for each combination of arms in order to determine the best superarm.
        :param rounds: number of simulations that must be run for each combinations of arms
        :return: a list containing the indexes of the best arms for each product according to the MC simulation.
        """
        simulation = Simulator(self.customer, self.graph, [1])
        maximum_estimate = -1  # assuming that a reward is a non negative number.
        best_super_arm = None
        for super_arm in self.super_arms:
            outcome = simulation.run(rounds, super_arm)
            reward = outcome.reward(super_arm)
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
        :return: a list conaining all the possible combinations.
        """
        if indexes is None:
            indexes = []
        if combinations is None:
            combinations = []
        if depth == self.n_products:
            combinations.append(indexes)
            return combinations
        new_depth = depth + 1
        for element in self.arms[depth]:
            new_indexes = indexes.copy()
            new_indexes.append(element)
            combinations = self._get_enumerations(new_depth, new_indexes, combinations)
        return combinations



