import numpy as np


class sparseSampling(object):
    """
        Implements a generic sparseSampling from "A Sparse Sampling Algorithm
        for Near-Optimal Planning in Large Markov Decision Processes
        M Kearns 2002"

        H = depth
        C = Width
        gamma = discount
        G = Model
        G must have following defined:
                1) G.transition(a) : Gets next state given action
                2) G.calcReward(a) : Calculates reward of doing action
                3) G.actions : list of all avaliable actions. Assumed fixed
                4) G.takeAction(a): Takes the action and transitions the state


    """

    def __init__(self, H, C, gamma, G, RmaX):
        super(sparseSampling, self).__init__()
        self.H = H
        self.C = C
        self.Rmax = Rmax
        self.gamma = gamma
        self.G = G
        self.s = G.curState
        self.Qstar = {}

    def estimateQ(self, h, s,):
        S_a = {}  # Holds next states
        q_h = {}  # Holds Q values from current state
        if h == 0:  # End recursion
            return [0.0] * len(self.G.actions)
        # Calculate next states
        for a in self.G.actions:  # For each action
            for c in range(0, self.C):  # Generate c children
                if (s, a) in S_a:  # If (s,a) already visited once
                    # Then append to the next state list
                    S_a[(s, a)].append(self.G.transition(a, s))
                else:
                    # Otherwise create a list containing the state
                    S_a[(s, a)] = [self.G.transition(a, s)]
        for a in self.G.actions:  # For each possible action
            tot = 0
            # Go through all possible sampled next states for each action
            for s_prime in S_a[(s, a)]:  # get the next state
                # Calculate according to the algorithm
                tot += self.estimateV(h - 1, s_prime)
            r = self.G.calcReward(s, a) + (self.gamma / self.C) * tot
            q_h[(s, a)] = r  # Updated reward for state action pair

        qStar = [0] * len(self.G.actions)
        for i, a in enumerate(self.G.actions):
            qStar[i] = q_h[(s, a)]

        return qStar

    def estimateV(self, h, s):
        qCur = self.estimateQ(h, s)
        return max(qCur)
