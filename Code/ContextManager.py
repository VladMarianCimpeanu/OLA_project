from Code.ReportSimulation import ReportSimulation
import numpy as np


class ContextManager(object):

    def __init__(self, learner_class, n_arms, n_products, customers, products_graph, prices, customers_distribution):
        self.t = 0
        self.history_rewards = []
        self.history_expected = []
        self.pulled = []
        self.aggregate_rewards = []  # i-th element contain the total reward got at day i

        self.n_arms = n_arms
        self.n_products = n_products
        self.customers = customers
        self.products_graph = products_graph
        self.prices = prices
        self.customers_distribution = customers_distribution
        self.get_learner = learner_class

        self.dict_reports = {customer.get_features(): [] for customer in customers}
        self.build_context()

    def update(self, pulled_arm, dict_report):
        """
        :param pulled_arm: list containing indexes of the pulled arms.
        :param dict_report: simulation report
        :return: None
        """
        current_features = [learner.get_customers()[0].get_features() for learner in self.tree.get_learners()]
        daily_reward = 0
        for features in current_features:
            prices = [self.prices[p][a] for p, a in enumerate(pulled_arm[features])]
            daily_reward += dict_report[features].reward(prices)

        self.aggregate_rewards.append(daily_reward)
        self.history_rewards.append({})
        self.history_expected.append({})
        self.pulled.append({})

        for features, report in dict_report.items():
            self.dict_reports[features].append((pulled_arm[features], report))
            self.tree.update(features, pulled_arm[features], report)

            prices = [self.prices[p][a] for p, a in enumerate(pulled_arm[features])]
            self.t += 1
            self.history_rewards[-1][features] = report.reward(prices)
            self.history_expected[-1][features] = report.expected_reward(prices)
            self.pulled[-1][features] = pulled_arm[features].copy()

    def select_superarm(self, rounds=100):
        """
        This method runs a montecarlo simulation for each combination of arms in order to determine the best superarm.
        :param rounds: number of simulations that must be run for each combinations of arms
        :return: a dictionary of lists containing the indexes of the best arms for each product according to the MC simulation as value and the users features as key.
        """
        return {k: self.tree.query(k) for k in self.dict_reports.keys()}

    def build_context(self):
        """
        Context generator algorithm called every two weeks
        """
        self.tree = ContextTree(self.get_learner,
                                dict_report=self.dict_reports,
                                n_arms=self.n_arms,
                                n_products=self.n_products,
                                customers=self.customers,
                                products_graph=self.products_graph,
                                prices=self.prices,
                                customers_distribution=self.customers_distribution,
                                left_indexes=[i for i in range(len(list(self.dict_reports)[0]))]
                                )


class ContextTree(object):
    def __init__(self, get_learner, dict_report, left_indexes, n_arms=None, n_products=None, customers=None,
                 products_graph=None, prices=None,
                 customers_distribution=None, root=None):
        """
        Constructor method of context tree object.
        :param get_learner: constructor method for the learner.
        :param dict_report: dictionary whose keys are tuples indicating the features of a customer,
        values a list of tuples (super_arm, report_object).
        :param n_arms: number of arms for each product.
        :param n_products: number of products.
        :param customers: set of customers for the subtree root learner.
        :param products_graph: product graph of the problem.
        :param prices: matrix with prices for each product-arm.
        :param customers_distribution: distribution of the set of customers for the subtree root learner.
        :param left_indexes: list containing the indexes of the features that has not been checked yet.
        :param root: learner at the root of the subtree.
        """
        self.get_learner = get_learner

        # don't split reward
        # root of the subtree: consider all the customers aggregate
        if root is None:
            self.learner = get_learner(n_arms, n_products, customers, products_graph, prices, customers_distribution)
            for values in dict_report.values():
                for pulled_arm, report in values:
                    self.learner.update(pulled_arm, report)
        else:
            self.learner = root

        # compute current best super arm and best reward for aggregate customer
        best_super_arm, best_maximum_estimate = self.learner.select_superarm(reward=True)
        best_split_info = None

        # select best split among the features that has not been checked yet in the higher levels of the tree.
        for feature_id in left_indexes:
            # build left node of the tree for feature at position feature_id
            l_customers_subset, l_distribution, l_prob = self.get_subset_customers(self.learner.get_customers(),
                                                                                   self.learner.get_customers_distribution(),
                                                                                   feature_id,
                                                                                   0)
            l_learner = get_learner(self.learner.get_n_arms(),
                                    self.learner.get_n_products(),
                                    l_customers_subset,
                                    self.learner.get_product_graph(),
                                    self.learner.get_prices(),
                                    l_distribution
                                    )
            l_dict_report = {k: [] for k in dict_report.keys()}
            # build right node of the tree for feature at position feature_id
            r_customers_subset, r_distribution, r_prob = self.get_subset_customers(self.learner.get_customers(),
                                                                                   self.learner.get_customers_distribution(),
                                                                                   feature_id,
                                                                                   1)
            r_learner = get_learner(self.learner.get_n_arms(),
                                    self.learner.get_n_products(),
                                    r_customers_subset,
                                    self.learner.get_product_graph(),
                                    self.learner.get_prices(),
                                    r_distribution
                                    )

            # useless split

            if l_prob == 0 or r_prob == 0:
                continue

            r_dict_report = {k: [] for k in dict_report.keys()}

            # train new learners with the reports of their parent.
            for features, values in dict_report.items():
                for pulled_arm, report in values:
                    if features[feature_id] == 0:
                        l_learner.update(pulled_arm, report)
                        l_dict_report[features].append((pulled_arm, report))
                    else:
                        r_learner.update(pulled_arm, report)
                        r_dict_report[features].append((pulled_arm, report))

            # compute the best estimates of the new learners.
            _, l_maximum_estimate = l_learner.select_superarm(reward=True)
            _, r_maximum_estimate = r_learner.select_superarm(reward=True)

            estimate_reward = l_maximum_estimate + r_maximum_estimate

            if estimate_reward > best_maximum_estimate:
                best_maximum_estimate = estimate_reward
                best_split_info = (l_dict_report, r_dict_report, feature_id, l_learner, r_learner)

        if best_split_info is None:  # no split
            self.l = None
            self.r = None
            self.feature_id = -1
        else:  # split
            l_dict_report, r_dict_report, feature_id, l_learner, r_learner = best_split_info
            new_indexes = left_indexes.copy()
            new_indexes.remove(feature_id)
            self.l = ContextTree(self.get_learner, l_dict_report, new_indexes.copy(), root=l_learner)
            self.r = ContextTree(self.get_learner, r_dict_report, new_indexes.copy(), root=r_learner)
            self.feature_id = feature_id
            self.learner = None

    def query(self, features, rounds=100):
        if self.learner is None:
            if features[self.feature_id] == 0:
                return self.l.query(features, rounds=rounds)
            else:
                return self.r.query(features, rounds=rounds)
        else:
            return self.learner.select_superarm(rounds=rounds)

    def update(self, features, pulled_arm, report):
        if self.learner is None:
            if features[self.feature_id] == 0:
                self.l.update(features, pulled_arm, report)
            else:
                self.r.update(features, pulled_arm, report)
        else:
            self.learner.update(pulled_arm, report)

    @staticmethod
    def get_subset_customers(customer_set, customers_distribution, feature_pos, feature_val):
        """
        Find the customers with the feature in position feature_pos set to feature_val.
        :param customer_set: set of customers to read.
        :param customers_distribution: original customers distribution.
        :param feature_pos: position of the feature that must be checked.
        :param feature_val: value of the feature to be kept.
        :return: return two lists. The first containing the customer set with the feature at feature position
        feature_pos set to feature_val. The second contains the new distribution of customer. Furthermore, it returns
        the probability to find feature_val in feature_pos
        """
        customer_subset = []
        distribution_subset = []
        p_true = 0
        for pos, c in enumerate(customer_set):
            feature = c.get_features()[feature_pos]
            if feature == feature_val:
                customer_subset.append(c)
                distribution_subset.append(customers_distribution[pos])
                p_true += customers_distribution[pos]
        return customer_subset, distribution_subset, p_true

    def get_learners(self, learners=None):
        if learners is None:
            learners = []
        if self.learner is None:
            self.l.get_learners(learners)
            self.r.get_learners(learners)
        else:
            learners.append(self.learner)
        return learners

    def __str__(self):
        return f'{self.feature_id}<{self.l}, {self.r}>'
