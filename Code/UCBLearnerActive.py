from cmath import inf
from distutils.util import convert_path
import numpy as np
from Code.UCBLearner import UCBLearner


class UCBLearnerActive(UCBLearner):
    """
    this class works in a non stationarity environment with an ACTIVE approach of select when to forget the old data.
    """
    def __init__(self, n_arms, n_products, customers, products_graph, prices, customers_distribution, splitter=5):
        super().__init__(n_arms, n_products, customers, products_graph, prices, customers_distribution)
        self.rewards = np.zeros((n_products, n_arms))
        self.splitter = splitter
        self.conv_rate_history = []
        for i in range(n_products):
            temp_array = []
            for j in range(n_arms):
                temp_array.append([])
            self.conv_rate_history.append(temp_array)

    def update(self, pulled_arm, report):
        self.change_detection_test(pulled_arm ,report)
        super().update(pulled_arm, report)

    # TODO set delta by finding the standard deviation of the convertion rate 
    def change_detection_test(self, pulled_arm, report):
        conv_rate = report.get_conversion_rate()
        for product, arm in enumerate(pulled_arm):
            delta = 0.3
            mean1, mean2 = 0, 0

            if len(self.conv_rate_history[product][arm]) > 10:
                last_conv_rates = self.conv_rate_history[product][arm][-self.splitter:]
                last_conv_rates.append(conv_rate[product])

                mean1 = np.mean(self.conv_rate_history[product][arm][:-self.splitter])

                mean2 = np.mean(last_conv_rates)

            if self.t>11 and (mean1 < mean2 - delta or mean1 > mean2 + delta) and not np.isinf(self.upper_bounds[product,arm]):
                #detected an abruth change
                print("abrupt change")
                self.t = 0
                self.means = np.zeros((self.n_products, self.n_arms))
                self.upper_bounds = np.full((self.n_products, self.n_arms), np.inf)
                self.seen = np.zeros((self.n_products, self.n_arms))
                self.conv_rate_history = []
                for i in range(self.n_products):
                    temp_array = []
                    for j in range(self.n_arms):
                        temp_array.append([])
                    self.conv_rate_history.append(temp_array)
            self.conv_rate_history[product][arm].append(conv_rate[product])

    def get_conv_rate_history(self):
        return self.conv_rate_history
            

class UCBLearnerActive2(UCBLearnerActive):
    def __int__(self, n_arms, n_products, customers, products_graph, prices, customers_distribution, splitter=5):
        super().__init__(n_arms, n_products, customers, products_graph, prices, customers_distribution, splitter)
        self.t_arms = np.zeros((n_products, n_arms))

    def change_detection_test(self, pulled_arm, report):
        conv_rate = report.get_conversion_rate()
        for product, arm in enumerate(pulled_arm):
            delta = 0.3
            mean1, mean2 = 0, 0

            if len(self.conv_rate_history[product][arm]) > 10:
                last_conv_rates = self.conv_rate_history[product][arm][-self.splitter:]
                last_conv_rates.append(conv_rate[product])

                mean1 = np.mean(self.conv_rate_history[product][arm][:-self.splitter])

                mean2 = np.mean(last_conv_rates)

            if self.t_arms[product, arm] > 11 and (mean1 < mean2 - delta or mean1 > mean2 + delta) and not np.isinf(
                    self.upper_bounds[product, arm]):
                # detected an abruth change
                print("abrupt change for product {}, arm {}".format(product, arm))
                self.t_arms[product, arm] = 0
                self.means[product, arm] = 0
                self.upper_bounds[product, arm] = np.inf
                self.seen[product, arm] = 0
                self.conv_rate_history[product][arm] = [conv_rate[product]]

        