import numpy as np

class Learner:
    def __init__(self, n_arms):
        self.n_arms = n_arms
        self.t = 0
        self.reward_per_arm = [[] for i in range(n_arms)] 
        self.collected_rewards = np.array([])

    def reset(self):
        self.__init__(self.n_arms, self.t)

    def update(self, pulled_arm, rewards):
        self.reward_per_arm[pulled_arm].append(reward)                       
        self.collected_rewards = np.append(self.collected_rewards, reward)