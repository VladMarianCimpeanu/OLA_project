import numpy as np
from Code import Learner


class TSLearner(Learner):
    def __init__(self, n_arms, n_products, customer, products_graph):
        super().__init__(n_arms, n_products, customer, products_graph)
        self.beta_parameters = np.ones((n_products, n_arms, 2))

    def pull_arm(self):
        "select the arm to pull accordingly to beta dist (alpha and beta params"
        idx = np.argmax(np.random.beta(self.beta_parameters[:, 0], self.beta_parameters[:, 1]))
        return idx

    def update(self, pulled_arm, reward):
        "update the alpha and beta parameter"
        self.t += 1
        self.update_observations(pulled_arm, reward)  # method of superclass
        # update a params
        self.beta_parameters[pulled_arm, 0] = self.beta_parameters[pulled_arm, 0] + reward
        self.beta_parameters[pulled_arm, 1] = self.beta_parameters[pulled_arm, 1] + 1.0 - reward
