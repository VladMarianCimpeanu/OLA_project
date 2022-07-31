import numpy as np
import utils


class Simulator:
    """
    This class is used both by the environment and the learners. The former uses this class to create a round,
    whereas the latter uses this class to run MC simulation in order to solve the combinatorial problem.
    The environment will use the real data of the problem, in contrast the learner will pass its believed values.
    """
    def __init__(self, customers, products_graph, customer_distribution):
        self.customers = customers
        self.products_graph = products_graph
        self.customers_distribution = customer_distribution

    def run(self, rounds):
        count_visits = np.array([])
        count_conversions = np.array([])
        count_sold_items = np.array([])
        for _ in range(rounds):
            index = utils.sample_categorical_distribution(self.customers_distribution)
            c = self.customers[index]
            visits, conversions, sold = self.run_customer(c)
            count_visits += visits
            count_conversions += conversions
            count_sold_items += sold
        return count_visits, count_conversions, count_sold_items

    def run_customer(self, c) -> list:
        """
        run simulation for a single customer. Stops when the customer sees all the products as primary or he decides
        to not buy any product.
        :param c:
        :return:
        """
        displayed_primary = np.array([])
        product = self._choose_primary(c)

    @staticmethod
    def _choose_primary(customer):
        distribution_alpha = customer.get_distribution_alpha()
        alphas = np.random.dirichlet(distribution_alpha)
        return utils.sample_categorical_distribution(alphas)