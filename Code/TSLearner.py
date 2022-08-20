import numpy as np
from Code.Learner import Learner


class TSLearner(Learner):
    def __init__(self, n_arms, n_products, customer, products_graph, prices):
        super().__init__(n_arms, n_products, customer, products_graph, prices)
        self.beta_parameters = np.ones((n_products, n_arms, 2))

    def estimate_conversion_rates(self):
        return np.random.beta(self.beta_parameters[:, :, 0], self.beta_parameters[:, :, 1])

    def update(self, pulled_arm, report):
        """
        update the alpha and beta parameter
        :param pulled_arm: arms pulled during the interaction with the environment.
        :param report: ReportSimulation object containing all the relevant information about the real interaction
        with the environment.
        :return:
        """
        self.update_observations(pulled_arm, report)  # method of superclass
        # update alpha and beta params
        seen = report.get_seen()
        bought = report.get_bought()
        for index, arm in enumerate(pulled_arm):
            self.beta_parameters[index, arm, 0] = self.beta_parameters[index, arm, 0] + bought[index]
            self.beta_parameters[index, arm, 1] = self.beta_parameters[index, arm, 1] + seen[index] - bought[index]


