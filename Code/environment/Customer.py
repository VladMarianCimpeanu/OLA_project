DATA_PATH = "Code/data/full_graph_customer.json"


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
    def __init__(self, feature_1, feature_2):
        self.feature_1 = feature_1
        self.feature_2 = feature_2

        def _init_customer(path=DATA_PATH):
            """
            read json for customers
            :return:
            """
            pass

    def get_features(self):
        pass

    def get_probability_buy(self, product):
        pass

    def get_probability_click(self, primary, secondary):
        """
        get probability to click the secondary product given that the user has seen primary prodcut and the user is
        observing the secondary product
        :param primary:
        :param secondary:
        :return:
        """

    def get_distribution_alpha(self):
        pass

    def get_num_prods_distribution(self):
        pass

    def get_num_prods(self):
        pass

    def set_probability_click(self):
        pass

    def set_probability_buy(self):
        pass

    def set_distribution_alpha(self):
        pass

    def set_num_prods(self):
        pass


