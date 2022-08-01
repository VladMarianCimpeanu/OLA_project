import logging

class ReportSimulation:
    """
    This class contains all the relevant information about a simulation.
    """

    def __init__(self, n_arms, debug=False):
        self.n_arms = n_arms
        self.counter_seen = [0] * n_arms
        self.counter_items_bought = [0] * n_arms
        self.counter_num_bought = [0] * n_arms
        self.graph = [[0] * n_arms] * n_arms
        self.debug = debug

    def seen(self, product_id):
        if self.debug:
            logging.info(f"seen: {self.product_id}")
        self.counter_seen[product_id] += 1

    def bought(self, product_id, amount):
        if self.debug:
            logging.info(f"bought: {self.product_id} {amount}")
        self.counter_items_bought[product_id] += 1
        self.counter_num_bought[product_id] += amount

    def move(self, primary, secondary):
        if self.debug:
            logging.info(f"bought: {self.primary} {self.secondary}")
        self.graph[primary][secondary] += 1

    def get_conversion_rate(self):
        return [bought / seen for bought, seen in zip(self.counter_items_bought, self.counter_seen)]

    def get_graph(self):
        return [[self.graph[primary][secondary] / self.counter_seen[primary]
                 for secondary in range(self.n_arms)
                 ]
                for primary in range(self.n_arms)
                ]

    def reward(self, pulled_arms):
        assert len(pulled_arms) == len(self.counter_items_bought)
        return sum([(arm+1)*num for arm, num in zip(pulled_arms, self.counter_items_bought)])