import numpy as np

from ..applicator import Applicator

__all__ = ['Landscape']

def varBernoulliMixture(w, p, max=False):
    w,p = np.asanyarray(w), np.asanyarray(p)
    u = w.dot(p)

    if max:
        p = np.zeros(p.shape)
        p[...] = u

    sumterm = p**2 + p*(1 - p)
    return w.dot(sumterm) - u**2

class Landscape(Applicator):
    @property
    def _iterable(self):
        return self.lands

    def __init__(self, name, lands, term=False):
        self.n = None
        self.pebbleSample = None

        self.name = name
        self.lands = lands
        self.term = term

    @property
    def endscapes(self):
        endscapes = set()
        for l in self.lands:
            endscapes.add(l.endscape)
        return endscapes

    @property
    def endlands(self):
        endlands = set()
        for e in self.endscapes:
            for l in e.lands:
                endlands.add(l)
        return endlands

    @property
    def weights(self):
        return self.aget('n', array=True)/self.n

    @property
    def pebbles(self):
        return self.aget('pebbles', flatten=True)

    @property
    def failedPebbles(self):
        return self.aget('failedPebbles', flatten=True)

    @property
    def successfulPebbles(self):
        return self.aget('successfulPebbles', flatten=True)

    def run(self, auto=False):
        if self.term:
            return

        self.n = 0
        for l in self.lands:
            self.n += l.run()

        if auto:
            self.setNextPebbleSample(n=auto)
            for endscape in self.endscapes:
                endscape.run(auto=auto)

    def chooseLands(self, n, p=None):
        if not self.lands:
            raise ValueError("self.lands is empty")

        return np.random.choice(self.lands, size=n, p=p)

    def initPebbles(self, *ns):
        if len(ns)==1:
           ns = ns*len(self.lands)
        elif len(ns) != len(self.lands):
            raise ValueError

        for l,n in zip(self.lands, ns):
            l.initPebbles(n)

    def setNextPebbleSample(self, n):
        # choose a sample of appropriate size
        self.pebbleSample = np.random.choice(self.successfulPebbles, size=n)
        for p in self.pebbleSample:
            p.land.addNewPebble(p.copy())

        # assign each of the sampled pebbles to its current land
        for land in self.endlands:
            land.setNewPebbles()

    def pebbleStats(self):
        stats = {}
        stats['p'] = len(self.successfulPebbles)/len(self.pebbles)

        return stats

    def save(self):
        return tuple(sav for sav in self.applyMethod('save'))

    def load(self, *landSav):
        self.applyMethod('load', *landSav, bcast=True)
        self.n = len(self.failedPebbles) + len(self.successfulPebbles)

    def expected(self):
        return self.weights.dot(self.aget('p', array=True))

    def sampleMean(self):
        return len(self.successfulPebbles)/len(self.pebbles)

    def sampleVar(self, ddof=0):
        mean = self.sampleMean()
        return (((1 - mean)**2)*len(self.successfulPebbles) + ((0 - mean)**2)*len(self.failedPebbles))/(self.n - ddof)

    def var(self, max=False):
        return varBernoulliMixture(self.weights, self.aget('p', array=True), max=max)

        # u = self.expected()
        # if max:
        #     return u*(1 - u)
        # else:
        #     p = self.aget('p', array=True)
        #     return (self.aget('n', array=True)/self.n).dot(p**2 + (p*(1 - p))**2) - u**2
