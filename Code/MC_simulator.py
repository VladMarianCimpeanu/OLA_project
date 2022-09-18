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

    def run_dp(self, super_arm):
        ans = 0
        for c, p in zip(self.customers, self.customers_distribution):
            @lru_cache(maxsize=None)
            def dp(primary, mask):
                mask |= 1 << primary
                ans = np.zeros(5)

                # expected amount of items bought
                if c.num_prods_distributions[primary][super_arm[primary]] > 1e-4:
                    ans[primary] = 1 / c.num_prods_distributions[primary][super_arm[primary]]
                else:
                    ans[primary] = 1e4
                # !!! this is always 1

                click_prob = [c.get_probability_click(primary, secondary) for secondary in self.products_graph[primary]]
                
                for secondary, edge_prob, λ in zip(self.products_graph[primary], click_prob, λ_SLOTS):
                    if (mask & (1 << secondary)) == 0:
                        ans += λ * edge_prob * dp(secondary, mask)

                ans *= c.get_probability_buy(primary, super_arm[primary])
                return ans

            for primary, alpha in enumerate(c.get_distribution_alpha()):
                ans += p * alpha * dp(primary, 0)
        return ans

    def run(self, rounds, super_arm):
        """
        run a simulation on the environment given a super arm of n round
        :param rounds:
        :param super_arm: prices selected
        :return: ReportSimulation instance based on the simulation
        """
        report = ReportSimulation(len(super_arm))
        for _ in range(rounds):
            index = sample_categorical_distribution(self.customers_distribution) #choose one customer
            c = self.customers[index] #select the customer chosen
            self.run_customer(c, super_arm, report)
        return report


    def run_customer(self, c, super_arm, report):
        """
        run simulation for a single customer. Stops when the customer sees all the products as primary, or he decides
        not to buy any product.
        :param c: customer instance
        :param super_arm: prices
        :param report: ReportSimulation instance with all the simulation informations updated at the end
        """
        displayed_primary = [False] * len(super_arm)
        product = self._choose_primary(c)
        report.update_starts(product)
        self.shopping_dfs(product, displayed_primary, report, super_arm, c)

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

    def shopping_dfs(self, primary, displayed_primary, report, super_arm, c):
        displayed_primary[primary] = True
        report.seen(primary)
        if np.random.random() < c.get_probability_buy(primary, super_arm[primary]):
            amount = c.get_num_prods(primary, super_arm[primary]) #1
            report.bought(primary, amount)
            click_prob = [c.get_probability_click(primary, secondary) for secondary in self.products_graph[primary]]
            for secondary, edge_prob, λ in zip(self.products_graph[primary], click_prob, λ_SLOTS):
                if not displayed_primary[secondary] and np.random.random() < λ * edge_prob:
                    report.move(primary, secondary)
                    self.shopping_dfs(secondary, displayed_primary, report, super_arm, c)


class MCSimulator(Simulator):
    """
    This class is used only the Learner class in order to solve the combinatorial problem of finding the best super arm
    through a Montecarlo simulation.
    """
    def __init__(self, customers, products_graph, customer_distribution=[1], iterations_per_prod=450):
        """
        :param customers: list of customers. This class expects the size of this list to be 1
        :param products_graph: graph of products as matrix.
        :param customer_distribution:  distribution of customers. By default it is set to [1] since this classe expects
        customers to be composed by just one customer.
        :param iterations_per_prod: iterations to be run from each seed. In this scenario, a seed is a starting product.
        """
        super().__init__(customers, products_graph, customer_distribution)
        self.t = 0
        self.iterations_per_prod = iterations_per_prod
        self.current_product = 0

    def run_customer(self, c, super_arm, report):
        displayed_primary = [False] * len(super_arm)
        self.current_product = self.t // self.iterations_per_prod
        report.update_starts(self.current_product)
        self.shopping_dfs(self.current_product, displayed_primary, report, super_arm, c)

    def run(self, rounds, super_arm):  
        report = ReportSimulation(len(super_arm))
        rounds = self.iterations_per_prod * len(super_arm)
        activations = []
        c = self.customers[0]
        for _ in range(rounds):
            self.run_customer(c, super_arm, report)
            self.t += 1
            if self.t // self.iterations_per_prod > self.current_product: # estimate reward starting from this product
                conversions = np.array(report.get_bought()) / self.iterations_per_prod 
                activations.append(conversions)
                report = ReportSimulation(len(super_arm))
        self.t = 0
        self.current_product = 0
        return activations

