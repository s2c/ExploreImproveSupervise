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

    def __init__(self, gamma, G, Rmax, epsilon, H=None, C=None, model = None):
        super(sparseSampling, self).__init__()
        self.epsilon = epsilon
        self.Rmax = Rmax
        self.gamma = gamma
        self.G = G
        self.s = G.curState
        self.Qstar = {}
        self.ldba = (epsilon * ((1 - gamma)**2)) / 4
        self.Vmax = Rmax / (1 - gamma)
        self.model = model
        # self.turns = 1
        if H is not None:
            self.H = H
        else:
            self.H = np.log(self.ldba / self.Vmax)
            self.H = np.ceil(self.H / np.log(self.gamma))
            self.H = int(self.H)
        if C is not None:
            self.C = C
        else:
            one = (self.Vmax / self.ldba)**2
            numActions = len(self.G.actions)
            two = (2 * self.H) * np.log((numActions *
                                         self.H * (self.Vmax**2)) / self.ldba**2)
            three = np.log(Rmax / self.ldba)
            self.C = np.ceil(one * (two + three))
            self.C = int(self.C)

    def estimateQ(self, h, s, turn=1):  # start with player 0's turn
        curTurn = turn
        S_a = {}  # Holds next states
        q_h = {}  # Holds Q values from current state
        if h == 0:  # End recursion
            if self.model is not None:
                return model(s)
            else:
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
                tot += self.estimateV(h - 1, s_prime, curTurn+1)
            r = self.G.calcReward(s, a) + (self.gamma / self.C) * tot
            q_h[(s, a)] = r  # Updated reward for state action pair

        qStar = [0] * len(self.G.actions)

        for i, a in enumerate(self.G.actions):
            qStar[i] = q_h[(s, a)]

        # return qStar
        # return np.sign(s) * max(np.multiply(qStar, np.sign(s)))
        return qStar

    def estimateV(self, h, s, curTurn):
        qCur = self.estimateQ(h, s, curTurn)
        # positive state = p1, negative state = p2
        # make it clearer
        # print(curTurn)
        # if s > 0:
        if curTurn % 2==1:
            return max(qCur)
        else:
            return min(qCur)
        # elif s==0:
        # print(type(qCur))
        # return max(np.multiply(qCur, np.sign(s)))
