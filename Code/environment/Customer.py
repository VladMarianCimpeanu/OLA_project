import json
import numpy as np
import os


DATA_PATH = "{}/../data/customer_classes.json".format(os.path.dirname(os.path.abspath(__file__)))
JSON_DATA = json.load(open(DATA_PATH, 'r'))['classes']


class Customer:
    """
    Let P_SEC be a secondary product, p_c the probability to click the product and p_p the probability to buy p_p as
    a primary product and p_b as the probability to buy P_SEC as a secondary product.
    Assuming that P_SEC has been displayed to the customer, then p_b = p_p * p_c.
    Given that P_SEC as been observed after buying another product P_PRIME, the probability to click P_SEC is
    p(P_SEC| P_PRIME).
    Finally p_c = p(P_SEC| P_PRIME) * lambda where lambda = 1 if P_SEC is in 1st slot, otherwise a fixed number in
    (0, 1)
    """

    def __init__(self, feature_1, feature_2, alpha=None, num_prods_distribution=None, click_graph=None,
                 buy_distribution=None):
        self.feature_1 = feature_1
        self.feature_2 = feature_2
        json_data = [w for w in JSON_DATA if w['features'] == [self.feature_1, self.feature_2]]
        if len(json_data) == 1:
            json_data = json_data[0]

        if alpha is None:
            alpha = json_data['alpha']
        if num_prods_distribution is None:
            num_prods_distribution = json_data['num_prods_distribution']
        if click_graph is None:
            click_graph = json_data['click_graph']
        if buy_distribution is None:
            buy_distribution = json_data['buy_distribution']

        self.alpha = alpha
        self.num_prods_distributions = num_prods_distribution
        self.click_graph = click_graph
        self.buy_distribution = buy_distribution

    def get_features(self):
        return self.feature_1, self.feature_2

    def get_probability_buy(self, product, price):
        return self.buy_distribution[product][price]

    def get_probability_click(self, primary, secondary):
        """
        get probability to click the secondary product given that the user has seen primary product and the user is
        observing the secondary product
        :param primary:
        :param secondary:
        :return:
        """
        return self.click_graph[primary][secondary]

    def get_click_graph(self):
        return self.click_graph

    def get_distribution_alpha(self):
        return self.alpha

    def get_num_prods_distribution(self):
        return self.num_prods_distributions

    def get_num_prods(self, product, price):
        return np.random.geometric(self.num_prods_distributions[product][price])

    def get_buy_distribution(self):
        return self.buy_distribution

    def set_probability_click(self, click_graph):
        self.click_graph = click_graph

    def set_probability_buy(self, buy_distribution):
        self.buy_distribution = buy_distribution

    def set_distribution_alpha(self, alpha):
        self.alpha = alpha

    def set_num_prods(self, num_prods_distributions):
        self.num_prods_distributions = num_prods_distributions

    def __str__(self):
        return f"Customer({self.feature_1}, {self.feature_2})"

    def __repr__(self):
        return self.__str__()