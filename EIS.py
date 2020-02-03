from valueIteration import valueIteration
from EISGame import EISGame
from discretizer import discretizer
from sparseSampling import sparseSampling
# from bisect import bisect_left
from sklearn.neighbors import NearestNeighbors
import numpy as np


class SLModel(object):
    """ SLModel"""

    def __init__(self, discretizer):
        super(SLModel, self).__init__()
        self.d = discretizer
        self.V = dict.fromkeys(self.d.statesActual, 0)
        # self.neigbours = None  # For nearest neighbours

    def getValue(self, state):
        stateActual = self.d.nearest(state)  # From the discretizer
        return self.V[stateActual]

    def updateValues(self, data, k=None):
        if k is None:  # defaults to 2
            k = 2

        data = dict(data)  # Covert to dictionary for the O(1) lookup
        altData = list(data.items())  # get (trainingdata,value) tuple
        trainStates, trainVals = zip(*altData)  # split it
        # # Second implementation
        # for state in self.V.keys():
        #     # find closest state in data
        #     closest = self.__findClosest(state, sortedData)
        #     self.V[state] = data[closest]
        # Alternate Implementation:
        # for state,value in data:
        #   self.V[self.d.nearest(state)] = value

        # # Nearest Neigbor implementation
        posNeighbours = NearestNeighbors(n_neighbors=k)
        negNeighbours = NearestNeighbors(n_neighbors=k)
        # split into positive states
        posStates = np.array(
            list(filter((0.0).__lt__, trainStates))).reshape(-1, 1)
        # split into negative states
        negStates = np.array(
            list(filter((0.0).__ge__, trainStates))).reshape(-1, 1)
        posNeighbours.fit(posStates)  # fit positive states
        negNeighbours.fit(negStates)  # fit negative states
        for state, value in self.V.items():  # for each discretized state
            tot = 0  # set curTotal to 0
            if state > 0:  # if state is positive
                # just gets indices of neighbours
                # Need to reshape and flatten for sklearn
                neighbours = posNeighbours.kneighbors(
                    np.array(state).reshape(1, -1))[1].flatten()
                for curNeighbour in neighbours:  # For each neighbour
                    # Get the value of the neighbour from the training data
                    tot += data[posStates[curNeighbour][0]]
            else:  # If negative, then use the neg neighbours
                neighbours = negNeighbours.kneighbors(
                    np.array(state).reshape(1, -1))[1].flatten()
                for curNeighbour in neighbours:
                    tot += data[negStates[curNeighbour][0]]

            self.V[state] = tot / k  # Average of k nearest
