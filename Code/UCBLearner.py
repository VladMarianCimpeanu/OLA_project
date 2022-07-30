import numpy as np
from Code import Learner

class UCBLearner(Learner):
    def __init__(self, n_arms):
        super().__init__(n_arms)
        self.means = np.zeros(n_arms)
        self.widths = np.array([np.inf for _ in range(n_arms)])

    def pull_arm():
        "select the arm to pull "
        idx = np.argmax(self.means+self.widths)
        return idx

    def update(self, pulled_arm, reward):
        "update "
        self.update_observations(pulled_arm, reward)  #method of superclass
        self.means[arm_pulled] = np.mean(self.reward_per_arm[arm_pulled])
        for idx in range(self.n_arms):  #get the upper confidece bound
            n = len(self.reward_per_arm[idx])
            if n>0:
                self.widths[idx] = np.sqrt(2*np.log(self.t)/n)
            else:
                self.widths[idx] = np.inf