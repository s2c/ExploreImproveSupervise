import numpy as np
from bisect import bisect_left


class valueIteration(object):
    """stateRange is a list with [low,high]
       numInterval = number of intervals
       we use numspace so we have to -1
   t: near 0 constant so to avoid 0+,0- errors

    """

    def __init__(self, G, stateRange=[None, None], numInterval=8, C=1000, gamma=0.5, discretizer=None):
        super(valueIteration, self).__init__()
        if discretizer is not None:
            self.statesActual = discretizer.statesActual
        else:
            self.statesActual = np.linspace(
                stateRange[0], stateRange[1], numInterval + 1)
        self.discretizer = discretizer
        self.numInterval = numInterval
        self.gap = self.statesActual[1] - self.statesActual[0]
        # initialize everything to 0 in the beginning
        self.V = dict.fromkeys(self.statesActual, 0)
        self.C = C
        self.G = G
        self.gamma = gamma

    def nearestState(self, curState):
        # Olog(n)
        if self.discretizer is None:
            # Basically a binary search because remainder breaks
            pos = bisect_left(self.statesActual, curState)
            if pos == 0:
                return self.statesActual[0]
            if pos == len(self.statesActual):
                return self.statesActual[-1]
            before = self.statesActual[pos - 1]
            after = self.statesActual[pos]
            if after - curState < curState - before:
                final = after
            else:
                final = before
            if final not in self.statesActual:
                print("something messed up")
            else:
                return final
        else:
            return self.discretizer.nearest(curState)

    def getSPrime(self, action, state):
        sPrime = self.G.transition(action, state)  # get next state
        sPrime = self.nearestState(sPrime)  # get nearest next state
        return sPrime

    def nextIteration(self):
        for state in self.statesActual:  # for each state
            r = [0] * len(self.G.actions)
            for i, action in enumerate(self.G.actions):  # for each action
                tot = 0
                for c in range(0, self.C):  # get reward for each child from previous estimate
                    tot += self.V[self.getSPrime(action, state)]  # add it to
                r[i] = self.G.calcReward(
                    action, state) + self.gamma * (tot / self.C)
            if state > 0:  # 0 is considered player 2's state to get lowerbound
                self.V[state] = max(r)
            else:
                self.V[state] = min(r)
