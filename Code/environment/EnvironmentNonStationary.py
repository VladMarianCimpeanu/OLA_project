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
        self.n_phase = len(self.customers_ns[0].get_buy_distribution())


    def round(self, pulled_arm):
        print("t: ", self.t)
        phase = self.t // self.abrupt_change_interval
        print("phase", phase)
        if phase > self.n_phase-1:
            phase = self.n_phase-1
        if self.simulator is None or phase != self.phase:
            print("set customer")
            self.customers = []
            for c in self.customers_ns:
                self.customers.append(
                    Customer(c.feature_1, c.feature_2, buy_distribution=c.get_buy_distribution()[phase])
                )
                print("conv_rate:",c.get_buy_distribution()[phase])
            self.phase = phase
            self.simulator = Simulator(self.customers, self.products_graph, self.customers_distribution)
        self.t += 1
        return super().round(pulled_arm)

    def get_actual_conv_rate(self):
        phase = self.t // self.abrupt_change_interval
        if phase > self.n_phase-1:
            phase = self.n_phase-1
        actual_conv_rates = []
        for c in self.customers_ns:
            actual_conv_rates.append(c.get_buy_distribution()[phase])
        return actual_conv_rates


    def estimate_clairvoyant(self, precision=10):
        best_super_arm = []
        best_reward = []
        best_expected_reward = []
        reward_per_arm = []
        for phase in range(len(self.customers_ns[0].get_buy_distribution())):
            self.customers = []
            for c in self.customers_ns:
                self.customers.append(
                    Customer(c.feature_1, c.feature_2, buy_distribution=c.get_buy_distribution()[phase])
                )
            a, b, c, d = super().estimate_clairvoyant(precision)
            best_super_arm.append(a)
            best_reward.append(b)
            best_expected_reward.append(c)
            reward_per_arm.append(d)
        return best_super_arm, best_reward, best_expected_reward, reward_per_arm

    def new_iteration(self):
        """
        a method to reset all parameters because of a new iteration
        """
        self.t = 0
        self.phase = 0
        self.customers = [
            Customer(0, 0),
            Customer(0, 1),
            Customer(1, 0),
            Customer(1, 1)]
        self.simulator = None

