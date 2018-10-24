import numpy as np
from scipy import stats as sts

from .pebble import Pebble

__all__ = ['Land']

class Land:
    def __init__(self, name, p, endscape=None, endweights=None, pebbles=None):
        self.result = None
        self._newPebbles = []

        self.name = name
        self.p = p
        self._successDist = sts.bernoulli(self.p)

        self.endscape = None
        self.endweights = None
        self.setEndscape(endscape, endweights)

        self.pebbles = None
        self.failedPebbles = None
        self.successfulPebbles = None
        if pebbles is not None:
            self.setPebbles(pebbles)

    def setEndscape(self, endscape=None, endweights=None):
        if (endscape is None) != (endweights is None):
            raise ValueError("Only one of (endscape, endweights) is None")

        if endscape is not None and (len(endscape.lands) != len(endweights)):
            raise ValueError("length of endscape.lands does not match length of endweights")

        self.endscape = endscape
        self.endweights = endweights

    def setPebbles(self, pebbles=None):
        self.pebbles = [] if pebbles is None else pebbles
        self.failedPebbles = None
        self.successfulPebbles = None

    def initPebbles(self, n):
        self.setPebbles([Pebble(self) for i in range(n)])

    def addNewPebble(self, pebble):
        self._newPebbles.append(pebble)

    def setNewPebbles(self):
        self.setPebbles(self._newPebbles)
        self._newPebbles = []

    def run(self):
        self.result = self._successDist.rvs(len(self.pebbles))

        # np.compress takes from an array based on a boolean mask
        self.failedPebbles = np.compress(np.logical_not(self.result), self.pebbles)
        self.successfulPebbles = np.compress(self.result, self.pebbles)

        self.setEndlands()

        return self.result.size

    def setEndlands(self):
        # mark the endlands of the failed pebbles
        for p in self.failedPebbles:
            p.fail()

        # sample an endland for each successful pebble
        for p,e in zip(self.successfulPebbles, self.chooseEndlands(self.successfulPebbles.size)):
            p.setLand(e)

    def chooseEndlands(self, n):
        if n:
            return self.endscape.chooseLands(n=n, p=self.endweights)
        else:
            return []

    def __str__(self):
        return '{obj.name}, p={obj.p}'.format(obj=self)
