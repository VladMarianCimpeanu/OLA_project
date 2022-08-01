import numpy as np
from utils import sample_categorical_distribution
import ReportSimulation
from environment.settings import λ_SLOTS


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

    def run(self, rounds, super_arm):
        report = ReportSimulation.ReportSimulation(super_arm)
        for _ in range(rounds):
            index = utils.sample_categorical_distribution(self.customers_distribution)
            c = self.customers[index]
            self.run_customer(c, super_arm, report)
        return report

    def run_customer(self, c, super_arm, report):
        """
        run simulation for a single customer. Stops when the customer sees all the products as primary, or he decides
        not to buy any product.

        :param c:
        :param super_arm:
        :param report:
        """

        displayed_primary = [False] * len(super_arm)

        def shopping_dfs(primary):
            displayed_primary[primary] = True
            report.seen(primary)
            if np.random.random() < c.get_probability_buy(primary, super_arm[primary]):
                amount = c.get_num_prods(primary, super_arm[primary])
                report.bought(primary, amount)
                click_prob = [c.get_probability_click(primary, secondary) for secondary in self.products_graph[primary]]
                for secondary, edge_prob, λ in zip(self.products_graph[primary], click_prob, λ_SLOTS):
                    if not displayed_primary[secondary] and np.random.random() < λ * edge_prob:
                        report.move(primary, secondary)
                        shopping_dfs(secondary)

        product = self._choose_primary(c)
        shopping_dfs(product)

    @staticmethod
    def _choose_primary(customer):
        distribution_alpha = customer.get_distribution_alpha()
        alphas = np.random.dirichlet(distribution_alpha)
        return sample_categorical_distribution(alphas)
