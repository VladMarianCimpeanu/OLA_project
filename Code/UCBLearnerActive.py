from cmath import inf
from distutils.util import convert_path
import numpy as np
from Code.UCBLearner import UCBLearner

class UCBLearnerActive(UCBLearner):
    """
    this class works in a non stationarity environment with an ACTIVE approach of select when to forget the old data. 
    To detect the abrupt change we each time look at the variance of the convertion_rate---> if the change is bigger it found an abruth change
    """
    def __init__(self, n_arms, n_products, customer, products_graph, prices):
        super().__init__(n_arms, n_products, customer, products_graph, prices)
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
            if (conv_rate[product] < self.means[product, arm] - delta or conv_rate[product] > self.means[product, arm] + delta) and not np.isinf(self.upper_bounds[product,arm]):
                #detected an abruth change
                print("abrupt change")
                self.means[product, arm] = 0
                self.upper_bounds[product, arm] = np.inf
                self.seen[product, arm] = 0
                self.conv_rate_history[product][arm] = []
            self.conv_rate_history[product][arm].append(conv_rate[product])
            

    def get_conv_rate_history(self):
        return self.conv_rate_history
            
            
        