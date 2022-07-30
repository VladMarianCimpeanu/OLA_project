import numpy as np
from Code import Learner

class GreedyLearner(Learner):
    def __init__(self, n_arms):
        super().__init__(n_arms)

    def pull_arm(self):
        "it should start from all lower prices, then pull one arm randomly each time (so increase its price) and evaluate it... each time increse just one until no improvement"

    def update(self, pulled_arm, reward):
        "update the prior parameter accordingly to the arm pulled"
        self.t += 1
        self.update_observations(pulled_arm, reward)  #method of superclass
        self.expected_rewards[pulled_arm] = (self.expected_rewards[pulled_arm]*(self.t - 1) + reward) / self.t  #avg of the exp value reward collected