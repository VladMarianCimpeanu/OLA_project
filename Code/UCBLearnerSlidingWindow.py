import numpy as np
from Code.UCBLearner import UCBLearner


class UCBLearnerSlidingWindow(UCBLearner):
    def __init__(self, n_arms, n_products, customer, products_graph, prices, window_size=10):
        super().__init__(n_arms, n_products, customer, products_graph, prices)
        self.reports = []
        self.window_size = window_size


    def update(self, pulled_arm, report):
        """
        update the confidence upper bounds of all arms and means of the pulled arms.
        :param pulled_arm: list containing indexes of the arms in the super arm.
        :param report: simulation report
        :return: None
        """

        seen = np.array(report.get_seen())
        bought = np.array(report.get_bought())

        self.reports.append((seen, bought, pulled_arm))
        if len(self.reports) > self.window_size:
            neg_seen, neg_bought, neg_pulled_arm = self.reports[0]
            self.reports = self.reports[1:]
            for product, arm in enumerate(neg_pulled_arm):
                self.seen[product, arm] -= neg_seen[product]

            for product, arm in enumerate(neg_pulled_arm):
                if self.seen[product, arm] > 0:
                    self.means[product, arm] = (self.means[product, arm] * (neg_seen[product] + self.seen[product, arm]) - neg_bought[
                        product]) / self.seen[product, arm]
                else:
                    self.means[product, arm] = 0
        super(UCBLearnerSlidingWindow, self).update(pulled_arm, report)