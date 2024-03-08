"""
NOTE: You are only allowed to edit this file between the lines that say:
    # START EDITING HERE
    # END EDITING HERE

This file contains the base Algorithm class that all algorithms should inherit
from. Here are the method details:
    - __init__(self, num_arms, horizon): This method is called when the class
        is instantiated. Here, you can add any other member variables that you
        need in your algorithm.
    
    - give_pull(self): This method is called when the algorithm needs to
        select an arm to pull. The method should return the index of the arm
        that it wants to pull (0-indexed).
    
    - get_reward(self, arm_index, reward): This method is called just after the 
        give_pull method. The method should update the algorithm's internal
        state based on the arm that was pulled and the reward that was received.
        (The value of arm_index is the same as the one returned by give_pull.)

We have implemented the epsilon-greedy algorithm for you. You can use it as a
reference for implementing your own algorithms.
"""

import numpy as np
import math
# Hint: math.log is much faster than np.log for scalars

class Algorithm:
    def __init__(self, num_arms, horizon):
        self.num_arms = num_arms
        self.horizon = horizon
    
    def give_pull(self):
        raise NotImplementedError
    
    def get_reward(self, arm_index, reward):
        raise NotImplementedError

# Example implementation of Epsilon Greedy algorithm
class Eps_Greedy(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # Extra member variables to keep track of the state
        self.eps = 0.1
        self.counts = np.zeros(num_arms)
        self.values = np.zeros(num_arms)
    
    def give_pull(self):
        if np.random.random() < self.eps:
            return np.random.randint(self.num_arms)
        else:
            return np.argmax(self.values)
    
    def get_reward(self, arm_index, reward):
        self.counts[arm_index] += 1
        n = self.counts[arm_index]
        value = self.values[arm_index]
        new_value = ((n - 1) / n) * value + (1 / n) * reward
        self.values[arm_index] = new_value

# START EDITING HERE
# You can use this space to define any helper functions that you need
def kl_div(x, y):
    if x == 0:
        return math.log(1/(1-y))
    elif x == 1:
        return math.log(1/y)
    else:
        return x * math.log(x/y) + (1-x) * math.log((1-x)/(1-y))

def get_kl_ucb(p, k):
    lb, ub = p, 1
    while ub - lb > 1e-2:
        mid = (lb + ub) / 2
        if kl_div(p, mid) > k:
            ub = mid
        else:
            lb = mid
    return lb if kl_div(p, (lb + ub) / 2) > k else (lb + ub) / 2
# END EDITING HERE

class UCB(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # START EDITING 
        self.num_pulls = np.zeros(num_arms)
        self.emp_prob = np.zeros(num_arms)
        self.ucb = np.ones(num_arms) * 10
        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        return np.argmax(self.ucb)
        # END EDITING HERE  
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        self.num_pulls[arm_index] += 1
        n = self.num_pulls[arm_index]
        self.emp_prob[arm_index] = ((n - 1) / n) * self.emp_prob[arm_index] + (1 / n) * reward
        idx = self.num_pulls != 0
        self.ucb[idx] = self.emp_prob[idx] + np.sqrt(2*math.log(np.sum(self.num_pulls))/self.num_pulls[idx])
        # END EDITING HERE


class KL_UCB(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # You can add any other variables you need here
        # START EDITING HERE
        self.num_pulls = np.zeros(num_arms)
        self.emp_prob = np.zeros(num_arms)
        self.kl_ucb = np.ones(num_arms) * 2
        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        return np.argmax(self.kl_ucb)
        # END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        self.num_pulls[arm_index] += 1
        n = self.num_pulls[arm_index]
        self.emp_prob[arm_index] = ((n - 1) / n) * self.emp_prob[arm_index] + (1 / n) * reward
        lnt = math.log(np.sum(self.num_pulls))
        for i in range(self.num_arms):
            if self.num_pulls[i]:
                self.kl_ucb[i] = get_kl_ucb(self.emp_prob[i], lnt / self.num_pulls[i])
        # END EDITING HERE

class Thompson_Sampling(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # You can add any other variables you need here
        # START EDITING HERE
        self.args = np.ones((num_arms, 2))
        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        return np.argmax(np.random.beta(self.args[:, 1], self.args[:, 0]))
        # END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        self.args[arm_index, reward] += 1
        # END EDITING HERE
