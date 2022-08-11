import logging


class ReportSimulation:
    """
    This class contains all the relevant information about a simulation.
    """
    def __init__(self, n_products, debug=False):
        self.n_products = n_products
        self.counter_seen = [0] * n_products
        self.counter_items_bought = [0] * n_products
        self.counter_num_bought = [0] * n_products
        self.graph = [[0] * n_products] * n_products
        self.counter_starts = [0] * n_products
        self.debug = debug

    def update_starts(self, id_product):
        """
        update the number of times a product is visited as first when entering the e-commerce
        :param id_product: id of the visited product
        :return: None
        """
        self.counter_starts[id_product] += 1

    def get_starts(self):
        """
        returns the number of times a product has been visited as first when entering the website
        :return: list of numbers containing the starts
        """
        return self.counter_starts

    def seen(self, product_id):
        if self.debug:
            logging.info(f"seen: {product_id}")
        self.counter_seen[product_id] += 1

    def bought(self, product_id, amount):
        if self.debug:
            logging.info(f"bought: {product_id} {amount}")
        self.counter_items_bought[product_id] += 1
        self.counter_num_bought[product_id] += amount

    def move(self, primary, secondary):
        if self.debug:
            logging.info(f"bought: {primary} {secondary}")
        self.graph[primary][secondary] += 1

    def get_conversion_rate(self):
        return [bought / seen for bought, seen in zip(self.counter_items_bought, self.counter_seen)]

    def get_graph(self):
        return [[self.graph[primary][secondary] / self.counter_seen[primary]
                 for secondary in range(self.n_products)
                 ]
                for primary in range(self.n_products)
                ]

    def reward(self, pulled_arms):
        assert len(pulled_arms) == len(self.counter_items_bought)
        return sum([(arm+1)*num for arm, num in zip(pulled_arms, self.counter_items_bought)])