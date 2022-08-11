import numpy as np
from MC_simulator import Simulator
import json


class Learner:
    def __init__(self, n_arms, n_products, customer, products_graph):
        """

        :param n_arms:
        :param n_products:
        :param customer: customer contains all the BELIVED information about the customer by the learner.
        The learner updates the customer's attributes that are not known. The base class assumes that only the conversion
        rate should be estimated, so no customer's attribute will be updated.
        :param products_graph: name of the json file in Code/data with all the relevant information
        about the products graph given by the business unit. The file must contain a key named 'graph', whereas its
        value is the graph in matrix form.
        """
        self.n_arms = n_arms
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

    def _load_products(self, name):
        file = open('Code/data/{}'.format(name))
        data = json.load(file)
        return data['graph']

    def reset(self):
        self.__init__(self.n_arms, self.t)

    def update(self, pulled_arm, report):
        pass

    def select_superarm(self):
        simulation = Simulator(self.customer, )
        pass
