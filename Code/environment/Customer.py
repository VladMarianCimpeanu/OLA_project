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

        def get_behaviour(f_1, f_2):
            "read json"
            pass
