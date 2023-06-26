#  Copyright (c). All Rights Reserved.
#  General Optimal control Problem Solver (GOPS)
#  Intelligent Driving Lab (iDLab), Tsinghua University
#
#  Creator: iDLab
#  Lab Leader: Prof. Shengbo Eben Li
#  Email: lisb04@gmail.com
#
#  Description: Noise Function
#  Update Date: 2021-03-10, Yuhang Zhang: Revise Codes


import numpy as np


class EpsilonScheduler:
    """
    Epsilon-greedy scheduler with epsilon schedule.
    """

    def __init__(self, EPS_START=0.9, EPS_END=0.05, EPS_DECAY=2000):
        self.start = EPS_START
        self.end = EPS_END
        self.decay = EPS_DECAY

    def sample(self, action, action_num, steps):
        """Choose an action based on epsilon-greedy policy.

        Args:
            action (any): Predicted action, usually greedy.
            action_num (int): Num of discrete actions.
            steps (int): Global training steps.

        Returns:
            any: Action chosen by psilon-greedy policy.
        """
        thresh = self.end + (self.start - self.end) * np.exp(-steps / self.decay)
        if np.random.random() > thresh:
            return action
        else:
            return np.random.randint(action_num)


class EpsilonGreedy:
    def __init__(self, epsilon, action_num):
        self.epsilon = epsilon
        self.action_num = action_num

    def sample(self, action):
        if np.random.random() > self.epsilon:
            return action
        else:
            return np.random.randint(self.action_num)


class GaussNoise:
    def __init__(self, mean, std):
        self.mean = mean
        self.std = std

    def sample(self, action):
        return action + np.random.normal(self.mean, self.std)
