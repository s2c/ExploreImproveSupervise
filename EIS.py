from valueIteration import valueIteration
from EISGame import EISGame
from discretizer import discretizer
from sparseSampling import sparseSampling
from bisect import bisect_left

class SLModel(object):
    """ SLModel"""

    def __init__(self, discretizer):
        super(SLModel, self).__init__()
        self.d = discretizer
        self.V = dict.fromkeys(self.d.statesActual, 0)

    def getValue(self, state):
        stateActual = self.d.nearest(state)
        return self.V[stateActual]

    def updateValues(self, data):

        ### first implementation
        data = dict(data)  # Covert to dictionary for the O(1) lookup
        sortedData = sorted(data.items()) # sort the data first
        sortedData, _ = zip(*sortedData)
       
        for state in self.V.keys():
            # find closest state in data
            closest = self.__findClosest(state, sortedData)
            self.V[state] = data[closest]
        ### Alternate Implementation:
        # for state,value in data:
        # 	self.V[self.d.nearest(state)] = value

    def __findClosest(self, point, sortedData):
        #sortedData = sorted(dataStates.items())
        #sortedData, _ = zip(*sortedData)
        pos = bisect_left(sortedData, point)
        if pos == 0:
            return sortedData[0]
        if pos == len(sortedData):
            return sortedData[-1]
        before = sortedData[pos - 1]
        after = sortedData[pos]
        if after - point < point - before:
            final = after
        else:
            final = before
        return final
