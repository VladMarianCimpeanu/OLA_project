from Code.ReportSimulation import ReportSimulation

class ContextManager(object):

    def __init__(self, learner_class, n_arms, n_products, customers, products_graph, prices, customers_distribution):
        self.get_learner = lambda: learner_class(n_arms, n_products, customers, products_graph, prices, customers_distribution)
        self.dict_reports = {customer.get_features(): [] for customer in customers}
        self.build_context()


    def update(self, pulled_arm, dict_report):
        """
        :param pulled_arm: list containing indexes of the pulled arms.
        :param report: simulation report
        :return: None
        """
        for features, report in dict_report.items():
            self.dict_reports[features].append((pulled_arm[features], report))
            self.tree.update(features, pulled_arm[features], report)


    def select_superarm(self, rounds=100):
        """
        This method runs a montecarlo simulation for each combination of arms in order to determine the best superarm.
        :param rounds: number of simulations that must be run for each combinations of arms
        :return: a dictionary of lists containing the indexes of the best arms for each product according to the MC simulation as value and the users features as key.
        """
        return {k: self.tree.query(k) for k in self.dict_reports.keys()}


    def build_context(self):
        '''
        Context generator algorithm called every two weeks
        '''
        self.tree = ContextTree(self.get_learner, dict_report=self.dict_reports)


class ContextTree(object):
    def __init__(self, get_learner, dict_report):
        self.get_learner = get_learner

        # don't split reward
        self.learner = get_learner()
        for values in dict_report.values():
            for pulled_arm, report in values:
                self.learner.update(pulled_arm, report)

        best_super_arm, best_maximum_estimate = self.learner.select_superarm(reward=True)
        best_split_info = None

        # select best split
        for feature_id in range(len(list(dict_report.keys())[0])):
            l_learner = get_learner()
            l_dict_report = {k: [] for k in dict_report.keys()}
            r_learner = get_learner()
            r_dict_report = {k: [] for k in dict_report.keys()}
            for features, values in dict_report.items():
                for pulled_arm, report in values:
                    if features[feature_id] == 0:
                        l_learner.update(pulled_arm, report)
                        l_dict_report[features].append((pulled_arm, report))
                    else:
                        r_learner.update(pulled_arm, report)
                        r_dict_report[features].append((pulled_arm, report))

            _, l_maximum_estimate = l_learner.select_superarm(reward=True)
            _, r_maximum_estimate = r_learner.select_superarm(reward=True)
            l_prob = 0
            r_prob = 0
            for idx, prob in enumerate(self.learner.customers_distribution):
                if (idx & (1 << feature_id)) == 0:
                    l_prob += prob
                else:
                    r_prob += prob
            assert abs(l_prob+r_prob-1) <= 1e-5
            estimate_reward = l_maximum_estimate * l_prob + r_maximum_estimate * r_prob
            if estimate_reward > best_maximum_estimate:
                best_maximum_estimate = estimate_reward
                best_split_info = (l_dict_report, r_dict_report, feature_id)

        if best_split_info is None: # no split
            self.l = None
            self.r = None
            self.feature_id = -1
        else: # split
            l_dict_report, r_dict_report, feature_id = best_split_info
            self.l = ContextTree(self.get_learner, l_dict_report)
            self.r = ContextTree(self.get_learner, l_dict_report)
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
                return self.l.query(features, pulled_arm, report)
            else:
                return self.r.query(features, pulled_arm, report)
        else:
            return self.learner.update(pulled_arm, report)

    def __str__(self):
        return f'{self.feature_id}<{self.l}, {self.r}>'