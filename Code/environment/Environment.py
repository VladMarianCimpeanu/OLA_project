import sys

import numpy as np
from Code.environment import settings
from Code.environment.Customer import Customer
import Code.utils as utils
from Code.MC_simulator import Simulator, MCSimulator
import json
import os


class Environment:
    def __init__(self, customers_behaviour, customers_per_day, variance_customers, p_lambda, products_graph, prices):
        """
        :param customers_behaviour: path file to customers behaviour
        :param customers_per_day:
        :param p_lambda: probability to observe second slot for secondary products
        :param products_graph: for each product this graph tells its secondary products and in which order.
        """
        self.customers_behaviour = customers_behaviour
        self.customers_per_day = customers_per_day
        self.variance_customers = variance_customers
        self.customers_distribution = settings.customers_distribution  # categorical distribution
        self.products_graph = self._init_products_graph(products_graph)
        self.p_lambda = p_lambda
        self.prices = prices
        self.simulator = None
        self.customers = [
            Customer(0, 0),
            Customer(0, 1),
            Customer(1, 0),
            Customer(1, 1)]

    @classmethod
    def _init_products_graph(cls, name):
        """
        read json for customers
        :return:
        """
        file_position = "{}/../data/{}".format(os.path.dirname(os.path.abspath(__file__)), name)
        file = open(file_position)
        data = json.load(file)
        return data['graph']

    def round(self, pulled_arm):
        """
        simulate the customer and return for each product the number of visits, the number of conversions(the user
        decides to buy one or more items of that product ---> always count 1) and the number
        of times it has been bought
        """
        number_customers = np.maximum(int(np.random.normal(self.customers_per_day, self.variance_customers)), 1)
        if self.simulator is None:
            self.simulator = Simulator(self.customers, self.products_graph, self.customers_distribution)
        return self.simulator.run(number_customers, pulled_arm)

    def _generate_customer(self):
        pass

    def get_aggregate_alphas(self):
        """
        Compute the values of alphas as weighted sum of them and normalize them such that their sum equals to 1.
        :return: list of alphas
        """
        weighted_alphas = []
        for index, customer in enumerate(self.customers):
            weighted_alphas.append(np.array(customer.get_distribution_alpha()) * self.customers_distribution[index])
        aggregate_alphas = np.array([0 for _ in range(len(weighted_alphas[0]))])
        for alphas in weighted_alphas:
            aggregate_alphas = aggregate_alphas + alphas
        # normalize alphas
        aggregate_alphas = aggregate_alphas / sum(aggregate_alphas)
        return aggregate_alphas

    def get_aggregate_num_prods_distribution(self):
        """
        Compute the aggregate parameters for the probability distribution about the number of items to buy for a
        specific product.
        :return: get a np.array containing all the aggregate probability distributions for each product for each arm.
        """
        current_distribution = np.zeros_like(self.prices)
        for index, customer in enumerate(self.customers):
            current_distribution = current_distribution + \
                                   np.array(customer.get_num_prods_distribution()) * self.customers_distribution[index]
        return current_distribution

    def get_aggregate_click_graph(self):
        """
        Compute the click graph for aggregate customers.
        :return: an np.array containing the click graph as matrix.
        """
        aggregate_graph = np.zeros((len(self.prices), len(self.prices)))
        for index, customer in enumerate(self.customers):
            aggregate_graph = aggregate_graph + np.array(customer.get_click_graph()) * self.customers_distribution[
                index]
        return aggregate_graph

    def _get_aggregate_buy(self):
        aggregate_buy = np.zeros_like(self.prices)
        for index, customer in enumerate(self.customers):
            aggregate_buy = aggregate_buy + np.array(customer.get_buy_distribution()) * self.customers_distribution[
                index]
        return aggregate_buy

    def estimate_clairvoyant(self, precision=10):
        """
        This method computes an estimate of the clairvoyant algorithm using MC simulatios.
        :param precision: integer representing the degree of precision for the estimate: higher is precision, higher is
        the precision of the estimate.
        By default, it is set to 10. Minimum required is 1.
        :return: the indexes of the best arm, the daily expected reward and the expected reward per customer
         for the clairvoyant algorithm.
        """
        assert precision > 0

        reward_per_arm = {}

        sim = Simulator(self.customers, self.products_graph, self.customers_distribution)
        best_reward = -1
        best_expected_reward = -1
        enumerations = self._get_enumerations()
        best_super_arm = None
        for iteration, super_arm in enumerate(enumerations):
            if iteration % 10 == 0:
                utils.progress_bar(iteration, len(enumerations))

            prices = [self.prices[p][a] for p, a in enumerate(super_arm)]

            expected_reward = self.customers_per_day * sum([price*num for price, num in zip(prices, sim.run_dp(super_arm))])
            '''
            mc = [sim.run(self.customers_per_day, super_arm).reward(prices) for _ in range(precision)]
            mc_reward = np.mean(mc)
            mc_std = np.std(mc)
            print(f'{super_arm}: {expected_reward} - {mc_reward} +- {mc_std}')
            '''

            reward_per_arm[tuple(super_arm)] = expected_reward

            if expected_reward > best_reward:
                best_reward = expected_reward
                best_expected_reward = expected_reward / self.customers_per_day
                best_super_arm = super_arm
        return best_super_arm, best_reward, best_expected_reward, reward_per_arm

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
        if depth == len(self.prices):
            combinations.append(indexes)
            return combinations
        new_depth = depth + 1
        for element in range(len(self.prices[0])):
            new_indexes = indexes.copy()
            new_indexes.append(element)
            combinations = self._get_enumerations(new_depth, new_indexes, combinations)
        return combinations


if __name__ == "__main__":
    file_customers = "customer_classes.json"
    file_products = "business_full_graph.json"
    mean = 100
    sigma = 20
    p_l = 0.5
    arms = [
        [20, 12, 15, 10],
        [3, 4, 1, 8],
        [24, 13, 18, 21],
        [15, 12, 18, 20],
        [12, 15, 19, 21]
    ]
    env = Environment(file_customers, mean, sigma, p_l, file_products, arms)
    print(env.get_aggregate_alphas())
    print(env.get_aggregate_num_prods_distribution())
