import numpy as np
from functools import lru_cache

from Code.utils import sample_categorical_distribution
from Code.ReportSimulation import ReportSimulation
from Code.environment.settings import λ_SLOTS


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
        """
        run a simulation on the environment given a super arm of n round
        :param rounds:
        :param super_arm: prices selected
        :return: ReportSimulation instance based on the simulation
        """
        report = ReportSimulation(len(super_arm))
        for _ in range(rounds):
            index = sample_categorical_distribution(self.customers_distribution)
            c = self.customers[index]
            self.run_customer(c, super_arm, report)
        return report

    def run_dp(self, super_arm):
        @lru_cache(maxsize=None)
        def dp(primary, mask):
            mask |= 1 << primary
            ans = np.zeros(5)

            # expected amount of items bought
            ans[primary] = 1 / c.num_prods_distributions[primary][super_arm[primary]]

            click_prob = [c.get_probability_click(primary, secondary) for secondary in self.products_graph[primary]]
            for secondary, edge_prob, λ in zip(self.products_graph[primary], click_prob, λ_SLOTS):
                if (mask & (1 << secondary)) == 0:
                    ans += λ * edge_prob * dp(secondary, mask)

            ans *= c.get_probability_buy(primary, super_arm[primary])
            ''''
            if np.any(np.isnan(ans)):
                print(ans, primary, super_arm, c.get_probability_buy(primary, super_arm[primary]))
                print(c.buy_distribution, primary, super_arm[primary])
            '''
            return ans

        ans = 0
        for c, p in zip(self.customers, self.customers_distribution):
            for primary, alpha in enumerate(c.get_distribution_alpha()):
                ans += p * alpha * dp(primary, 0)
        return ans

    def run_customer(self, c, super_arm, report):
        """
        run simulation for a single customer. Stops when the customer sees all the products as primary, or he decides
        not to buy any product.
        :param c: customer instance
        :param super_arm: prices
        :param report: ReportSimulation instance with all the simulation informations updated at the end
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
        report.update_starts(product)
        shopping_dfs(product)

    @staticmethod
    def _choose_primary(customer):
        """
        select the primary product based on the alpha paramether of the specific customer and then return the index of the chosen product
        :param customer: user interacting
        :return : index of selected product
        """
        distribution_alpha = customer.get_distribution_alpha()
        alphas = np.random.dirichlet(distribution_alpha)
        return sample_categorical_distribution(alphas)
