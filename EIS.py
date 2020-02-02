from valueIteration import valueIteration
from EISGame import EISGame
from discretizer import discretizer
from sparseSampling import sparseSampling


class SLModel(object):
	"""docstring for model"""
	def __init__(self,discretizer):
		super(SLModel, self).__init__()
		self.d = discretizer
		self.V = dict.fromkeys(self.d.statesActual,0)

	def getValue(self,state):
		stateActual = self.d.nearest(state)
		return self.V[stateActual]

	def updateValues(self,data):
		for state,value in data:
			self.V[self.d.nearest(state)] = value
