from cmath import inf
from distutils.util import convert_path
import numpy as np
from Code.UCBLearner import UCBLearner

class UCBLearnerActive(UCBLearner):
    """
    this class works in a non stationarity environment with an ACTIVE approach of select when to forget the old data. 
    To detect the abrupt change we each time look at the variance of the convertion_rate---> if the change is bigger it found an abruth change
    """
    def __init__(self, n_arms, n_products, customers, products_graph, prices, customers_distribution, splitter=10):
        super().__init__(n_arms, n_products, customers, products_graph, prices, customers_distribution)
        self.rewards = np.zeros((n_products, n_arms))
        self.slpitter = splitter
        self.seen = np.zeros((n_products, n_arms))
        self.conv_rate_history = []
        for i in range(n_products):
            temp_array = []
            for j in range(n_arms):
                temp_array.append([])
            self.conv_rate_history.append(temp_array)
            


    def update(self, pulled_arm, report):
        self.change_detection_test(pulled_arm ,report)
        for p,a in enumerate(pulled_arm):
            prices = [prices[p][a]]
            self.rewards[p][a] += report.reward(prices)
            self.seen[p][a] += report.get_seen()[p]
        super().update(pulled_arm, report)

    # TODO set delta by finding the standard deviation of the convertion rate 
    def change_detection_test(self, pulled_arm, report):
        conv_rate = report.get_conversion_rate()
        for product, arm in enumerate(pulled_arm):
            delta = 0.3

            if (conv_rate[product] < self.means[product, arm] - delta or conv_rate[product] > self.means[product, arm] + delta) and not np.isinf(self.upper_bounds[product,arm]) and self.t>35:
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
                self.rewards = np.zeros((n_products, n_arms))
                self.seen = np.zeros((n_products, n_arms))
            self.conv_rate_history[product][arm].append(conv_rate[product])
            

    def get_conv_rate_history(self):
        return self.conv_rate_history
            
            
        