import numpy as np
from Code.Learner import Learner
from Code.TSLearner import TSLearner

class TSLearner4(TSLearner):
    def __init__(self, n_arms, n_products, customer, products_graph, prices):
        super().__init__(n_arms, n_products, customer, products_graph, prices)
        self.estimated_alphas = np.zeros(n_products)
        self.estimated_n_items = np.zeros((n_products,n_arms))  #number of time each prod has been bought
        self.estimated_n_bought = np.zeros((n_products,n_arms)) #quantity of items bought
        self.mean_items = np.zeros((n_products,n_arms))


    def update(self, pulled_arm, report):
        """
        Override of the update method of TSLearner class
        here this class also estimates the alpha ratios and the number of items sold per product
        """
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
        #we have to compute the inverse of the mean for each value different from 0
        new_mean = self.mean_items.copy()
        new_mean[new_mean>0] = 1 / new_mean[new_mean>0]
        #print("inverted mean: ", new_mean)
        self.customer.set_num_prods(new_mean)