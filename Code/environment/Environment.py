import numpy as np
from Code.environment import settings
from Code.environment.Customer import Customer
import Code.utils
from Code.MC_simulator import Simulator
import json


class Environment:
    def __init__(self, customers_behaviour, customers_per_day, variance_customers, p_lambda, products_graph):
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
        self.simulator = None
        self.customers = [
                Customer(0, 0),
                Customer(0, 1),
                Customer(1, 0),
                Customer(1, 1)
            ]

    def _init_products_graph(self, name):
        """
        read json for customers
        :return:
        """
        file = open('Code/data/{}'.format(name))
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
            self.simulator = Simulator(self.customers, self.graph, self.customers_distribution)
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
        pass

    def get_aggregate_click_graph(self):
        pass

    def get_aggregate_buy_distribution(self):
        pass


