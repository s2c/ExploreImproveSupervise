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
                3) G.actions : list of all avaliable actions
                4) G.takeAction(a): Takes the action and transitions the state


    """

    def __init__(self, H, C, gamma, G):
        super(sparseSampling, self).__init__()
        self.H = H
        self.C = C
        self.gamma = gamma
        self.G = G
        self.s = G.curState
        self.Qstar = {}
        self.Vstar = [0] * self.H

    def Q(self, s, a, r):
        if (s, a) in self.Qstar:
            self.Qstar[(s, a)].append(r)
        else:
            self.Qstar[(s, a)] = [r]

    def estimateQ(self, h, s):
        S_a = {}
        if h == 0:
            return 0
        for a in self.G.actions:
            for c in range(0, self.C):
                if (s, a) in S_a:
                    S_a[(s, a)].append(G.transition(a, s))
                else:
                    S_a[(s, a)] = [G.transition(a, s)]
        return S_a

                # r = G.calcReward(G.curState, a) + \
                #     (self.gamma / self.C) * sum(self.estimateV(h - 1,))
                # self.Q(s, a, r)
