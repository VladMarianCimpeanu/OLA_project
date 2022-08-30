from Code.environment.Environment import Environment
from Code.environment.Customer import Customer
from Code.MC_simulator import Simulator
import Code.environment.settings as settings
import os


DATA_PATH = "{}/../data/customer_n_s.json".format(os.path.dirname(os.path.abspath(__file__)))

class EnvironmentNonStationary(Environment):
    def __init__(self, customers_behaviour, customers_per_day, variance_customers, p_lambda, products_graph, prices,
                 abrupt_change_interval):
        super().__init__(customers_behaviour, customers_per_day, variance_customers, p_lambda, products_graph, prices)
        self.abrupt_change_interval = abrupt_change_interval
        self.customers_ns = [
            Customer(0, 0, file_name=DATA_PATH),
            Customer(0, 1, file_name=DATA_PATH),
            Customer(1, 0, file_name=DATA_PATH),
            Customer(1, 1, file_name=DATA_PATH)
        ]
        self.t = 0
        self.phase = 0


    def round(self, pulled_arm):
        phase = self.t // self.abrupt_change_interval
        if self.simulator is None or phase != self.phase:
            self.customers = []
            for c in self.customers_ns:
                self.customers.append(
                    Customer(c.feature_1, c.feature_2, buy_distribution=c.get_buy_distribution()[phase])
                )
            self.phase = phase
            self.simulator = Simulator(self.customers, self.products_graph, self.customers_distribution)
        return super().round(pulled_arm)