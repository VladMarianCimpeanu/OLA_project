import numpy as np
from Code.environment import settings
from Code.environment.Customer import Customer
import Code.utils
from Code.MC_simulator import Simulator
import json
import os


class Environment:
    def __init__(self, customers_behaviour, customers_per_day, variance_customers, p_lambda, products_graph, arms):
        """
        :param customers_behaviour: path file to customers behaviour
        :param customers_per_day:
        :param p_lambda: probability to observe second slot for secondary products
        :param products_graph: for each product this graph tells its secondary products and in which order.
        """
        self.customers_behaviour = customers_behaviour
        self.customers_per_day = customers_per_day
        self.variance_customers = variance_customers
        self.customers_distribution = [1]
        #self.customers_distribution = settings.customers_distribution  # categorical distribution
        self.products_graph = self._init_products_graph(products_graph)
        self.p_lambda = p_lambda
        self.arms = arms
        self.simulator = None
        self.customers = [
            Customer(0, 0)]
 #           Customer(0, 1),
 #           Customer(1, 0),
 #           Customer(1, 1)

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
        current_distribution = np.zeros_like(self.arms)
        for index, customer in enumerate(self.customers):
            current_distribution = current_distribution + \
                                   np.array(customer.get_num_prods_distribution()) * self.customers_distribution[index]
        return current_distribution

    def get_aggregate_click_graph(self):
        """
        Compute the click graph for aggregate customers.
        :return: an np.array containing the click graph as matrix.
        """
        aggregate_graph = np.zeros((len(self.arms), len(self.arms)))
        for index, customer in enumerate(self.customers):
            aggregate_graph = aggregate_graph + np.array(customer.get_click_graph()) * self.customers_distribution[
                index]
        return aggregate_graph

    def _get_aggregate_buy(self):
        aggregate_buy = np.zeros_like(self.arms)
        for index, customer in enumerate(self.customers):
            aggregate_buy = aggregate_buy + np.array(customer.get_buy_distribution()) * self.customers_distribution[
                index]


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
