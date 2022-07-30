import numpy as np

class Environment:
    def __init__(self, n_arms, probabilities):
        self.n_arms = n_arms
        self.probabilities = probabilities

    def round(self, pulled_arm, customer):
        " simulate the customer and return the reward (=number of item bought)"