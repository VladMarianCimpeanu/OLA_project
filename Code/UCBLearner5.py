import numpy as np
from Code.Learner import Learner
from Code.UCBLearner import UCBLearner

class UCBLearner5(UCBLearner):
    def __init__(self, n_arms, n_products, customer, products_graph, prices):
        super().__init__(n_arms, n_products, customer, products_graph, prices)
        self.estimated_graph = np.zeros((n_products,n_products))
        self.n_bought = np.array([0] * n_products)

    def update(self, pulled_arm, report):
        super().update(pulled_arm, report)
        n_clicks = np.array(report.get_clicks())
        print(n_clicks)
        print("---------")
        new_n_bought = np.array(report.get_bought())
        print(new_n_bought)
        print("---------")
        for i in range(self.n_products):
            if self.n_bought[i] + new_n_bought[i] > 0:
                self.estimated_graph[i,:] = (self.estimated_graph[i,:] * self.n_bought[i] + n_clicks[i,:]) / (self.n_bought[i] + new_n_bought[i])

        self.n_bought += new_n_bought

        print(self.estimated_graph)
        self.customer.set_probability_click(self.estimated_graph)
        