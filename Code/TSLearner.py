import numpy as np
from Code.Learner import Learner


class TSLearner(Learner):
    def __init__(self, n_arms, n_products, customers, products_graph, prices, customers_distribution):
        super().__init__(n_arms, n_products, customers, products_graph, prices, customers_distribution)
        self.beta_parameters = np.ones((n_products, n_arms, 2))

    def estimate_conversion_rates(self):
        return np.random.beta(a=self.beta_parameters[:, :, 0], b=self.beta_parameters[:, :, 1])

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

    def get_betas(self, prod, arm):
        return self.beta_parameters[prod, arm, :]


if __name__ == "__main__":
    betas = np.ones((3, 4, 2))
    betas[0, 0, 1] = betas[0, 0, 1] + 2
    print(betas)