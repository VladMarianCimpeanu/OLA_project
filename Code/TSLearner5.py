import numpy as np
from Code.TSLearner import TSLearner


class TSLearner5(TSLearner):
    def __init__(self, n_arms, n_products, customers, products_graph, prices, customers_distribution):
        super().__init__(n_arms, n_products, customers, products_graph, prices, customers_distribution)
        self.estimated_graph = np.zeros((n_products,n_products))
        self.n_bought = np.array([0] * n_products)

    def update(self, pulled_arm, report):
        super().update(pulled_arm, report)
        n_clicks = np.array(report.get_clicks())
        new_n_bought = np.array(report.get_bought())
        for i in range(self.n_products):
            if self.n_bought[i] + new_n_bought[i] > 0:
                self.estimated_graph[i,:] = (self.estimated_graph[i,:] * self.n_bought[i] + n_clicks[i,:]) / (self.n_bought[i] + new_n_bought[i])

        self.n_bought += new_n_bought
        self.customer.set_probability_click(self.estimated_graph)
        
