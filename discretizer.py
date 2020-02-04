from bisect import bisect_left
import numpy as np


class discretizer(object):
    """docstring for discretizer"""

    def __init__(self, stateRange, numIntervals):
        super(discretizer, self).__init__()
        self.stateRange = stateRange
        self.numInterval = numIntervals
        self.statesActual = self.discretize(stateRange)

    def discretize(self, stateRange=None):
        if stateRange is None:
            #self.statesActual = np.linspace(
            #    self.stateRange[0], self.stateRange[1], self.numInterval + 1)
            self.statesActual = np.array(list(np.linspace(-self.stateRange[1], -self.stateRange[0], self.numInterval+1))\
                + list(np.linspace(self.stateRange[0],self.stateRange[1],self.numInterval+1)))
        else:
            #self.statesActual = np.linspace(
            #    stateRange[0], stateRange[1], self.numInterval + 1)
            self.statesActual = np.array(list(np.linspace(-self.stateRange[1], -self.stateRange[0], self.numInterval+1))\
                + list(np.linspace(self.stateRange[0],self.stateRange[1],self.numInterval+1)))
        return self.statesActual

    def nearest(self, curState):
        # Basically a binary search because remainder breaks
        # where in the sorted listed to insert
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
