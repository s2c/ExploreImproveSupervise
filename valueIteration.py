import numpy as np

class valueIteration(object):
	"""stateRange is a list with [low,high]
	   numInterval = number of intervals
	   we use numspace so we have to -1
       t: near 0 constant so to avoid 0+,0- errors

	"""
	def __init__(self, stateRange=[None,None],numInterval=8, C = 1000):
		super(valueIteration, self).__init__()
		self.statesActual = np.linspace(stateRange[0],stateRange[1],numInterval+1)		
		self.numInterval = numInterval
		self.gap = self.statesActual[1]-self.statesActual[0]
		self.V = dict.fromkeys(v.statesActual,0) # initialize everything to 0 in the beginning
		self.C = C

	def nearestState(self, curState):
		# Cleaner nearest neighbour cause single dimensional
		if (curState % self.gap) > 0.5 * self.gap:
			nearest = curState - (curState % diff) + diff
		else:
			nearest = curState - (curState % diff)
		
		if nearest in self.statesActual:
			return nearest
		else:
			print ("Something messed up")
			return -4

	def Bellman(self,curState):
		pass





