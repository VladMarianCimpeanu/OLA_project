import numpy as np
import settings
from Code.environment.Customer import Customer


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
        self.p_lambda = p_lambda

    def _init_products_graph(self):
        """
        read json for customers
        :return:
        """
        pass

    def round(self, pulled_arm, customer=None) -> list:
        """
        simulate the customer and return for each product the number of visits, the number of conversions(the user
        decides to buy one or more items of that product ---> always count 1) and the number
        of times it has been bought
        """
        number_customers = np.maximum(int(np.random.normal(self.customers_per_day, self.variance_customers)), 1)
        if customer is None:
            customers = [
                Customer(0, 0),
                Customer(0, 1),
                Customer(1, 0),
                Customer(1, 1)
            ]
        else:
            customers = [customer] * len(self.customers_distribution)

    def _generate_customer(self):
        pass


