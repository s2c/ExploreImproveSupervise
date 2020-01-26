import numpy as np


class sparseSampling(object):
    """
        Implements a generic sparseSampling from "A Sparse Sampling Algorithm
        for Near-Optimal Planning in Large Markov Decision Processes
        M Kearns 2002"

    """

    def __init__(self, simulator=None):
        super(sparseSampling, self).__init__()
        self.arg = arg
