import numpy as np
from Code.Learner import Learner
from Code.UCBLearner import UCBLearner

class UCBLearner4(UCBLearner):
    def __init__(self, n_arms, n_products, customer, products_graph, prices):
        super().__init__(n_arms, n_products, customer, products_graph, prices)
        self.estimated_alphas = np.zeros(n_products)
        self.estimated_n_items = np.zeros((n_products,n_arms))
        self.estimated_n_bought = np.zeros((n_products,n_arms))
        self.mean_items = np.zeros((n_products,n_arms))


    def update(self, pulled_arm, report):
        print("customer alpha:", self.customer.get_distribution_alpha()) # TODO at first iteration it is set with the values in json file
        super().update(pulled_arm, report)
        self.estimated_alphas = self.estimated_alphas + np.array(report.get_starts())
        self.customer.set_distribution_alpha(self.estimated_alphas / sum(self.estimated_alphas))

        seen = self.estimated_n_items.copy() #old quantity
        bought = report.get_amount_bought()
        for p, a in enumerate(pulled_arm):
            self.estimated_n_items[p,a] += report.get_bought()[p] #new quantity
            self.estimated_n_bought[p,a] += report.get_amount_bought()[p]


            if self.estimated_n_items[p,a] > 0:
                self.mean_items[p,a] = (self.mean_items[p,a] * seen[p,a] + bought[p]) / (self.estimated_n_items[p,a])

        #print("mean: " , self.mean_items)
        new_mean = self.mean_items.copy()
        new_mean[new_mean>0] = 1 / new_mean[new_mean>0]
        #print("inverted mean: ", new_mean)
        self.customer.set_num_prods(new_mean)


        



