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
        self.graph = [[0] * n_products for _ in range(n_products)]
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
        """
        Update the number of times a given product has been seen during the simulation.
        :param product_id: index of the product
        :return: None
        """
        if self.debug:
            logging.info(f"seen: {product_id}")
        self.counter_seen[product_id] += 1

    def bought(self, product_id, amount):
        """
        Update the number of times a product has been bought during the simulation.
        This method updates both the counter about the conversion rates and the one about the total amount of items
        bought.
        :param product_id: index of the product.
        :param amount: number of units bought for that item
        :return: None
        """
        if self.debug:
            logging.info(f"bought: {product_id} {amount}")
        self.counter_items_bought[product_id] += 1
        self.counter_num_bought[product_id] += amount

    def move(self, primary, secondary):
        """
        Update the number of times an edge has been activated. An edge is a click on a secondary product
        given that the customer has seen a given primary product.
        :param primary: index of product from which the interaction started.
        :param secondary: index of product clicked.
        :return: None
        """
        if self.debug:
            logging.info(f"bought: {primary} {secondary}")
        self.graph[primary][secondary] += 1

    def get_conversion_rate(self):
        """
        Compute the conversion rates.
        :return: list containing conversion rates in the last simulation.
        """
        return [bought / seen for bought, seen in zip(self.counter_items_bought, self.counter_seen)]

    def get_seen(self):
        return self.counter_seen

    def get_bought(self):
        #return the number of times each item has been bought
        return self.counter_items_bought

    def get_amount_bought(self):
        #return the total amount of items bought
        return self.counter_num_bought

    def get_clicks(self):
        return self.graph

    def get_graph(self):
        # TODO: this does not consider if the customer has seen or not the secondary product. DISCUSS
        return [[self.graph[primary][secondary] / self.counter_seen[primary]
                 for secondary in range(self.n_products)
                 ]
                for primary in range(self.n_products)
                ]


    def reward(self, prices):
        """
        Compute the total reward achieved during the simulation
        :param prices: list containing the prices for each product.
        :return: return a floating point representing the total reward achieved during the simulation.
        """
        assert len(prices) == len(self.counter_num_bought)
        return sum([price * num for price, num in zip(prices, self.counter_num_bought)])

    def expected_reward(self, prices):
        num_customers = sum(self.counter_starts)
        return self.reward(prices) / num_customers
