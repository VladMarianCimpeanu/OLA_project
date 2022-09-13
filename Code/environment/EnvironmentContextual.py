from Code.environment.Environment import Environment
from Code.environment.Customer import Customer
from Code.MC_simulator import Simulator
import Code.environment.settings as settings
import os
import numpy as np
from Code.utils import sample_categorical_distribution
import collections
DATA_PATH = "{}/../data/customer2.json".format(os.path.dirname(os.path.abspath(__file__)))


class EnvironmentContextual(Environment):
    def __init__(self, customers_behaviour, customers_per_day, variance_customers, p_lambda, products_graph, prices):
        super().__init__(customers_behaviour, customers_per_day, variance_customers, p_lambda, products_graph, prices)

    def round(self, pulled_arm):
        total_number_customers = np.maximum(int(np.random.normal(self.customers_per_day, self.variance_customers)), 1)
        counter_customers = collections.Counter([sample_categorical_distribution(self.customers_distribution) for _ in range(total_number_customers)])

        ans = {}
        for customer in self.customers:
            customer_id = customer.get_features_id()
            number_customers = counter_customers.get(customer_id)
            if number_customers is None:
                number_customers = 0
            simulator = Simulator(customers=[customer], customer_distribution=[1], products_graph=self.products_graph)
            report = simulator.run(number_customers, pulled_arm[customer.get_features()])
            ans[customer.get_features()] = report
        return ans

    def estimate_clairvoyant(self, precision=10):
        print([customer.buy_distribution for customer in self.customers])
        best_super_arm, best_reward, best_expected_reward, reward_per_arm = {}, {}, {}, {}
        for customer in self.customers:
            best_super_arm[customer.get_features()], \
            best_reward[customer.get_features()], \
            best_expected_reward[customer.get_features()], \
            reward_per_arm[customer.get_features()] = super().estimate_clairvoyant(precision=precision, customers=[customer])
        return best_super_arm, best_reward, best_expected_reward, reward_per_arm

    def estimate_clairvoyant_reward(self, precision=10):
        pass
