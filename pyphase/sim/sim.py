import numpy as np

from ..applicator import Applicator

__all__ = ['Sim']

class Sim(Applicator):
    regionType = None

    @property
    def _iterable(self):
        return self.regions

    @property
    def expected(self):
        return self.aget('expected')

    @property
    def cov(self):
        return np.cov(self.expected)

    def __init__(self, reps, N, *args, **kwargs):
        self.regions = [self.regionType(N, *args, **kwargs) for i in range(reps)]

    def save(self):
        return tuple(sav for sav in self.applyMethod('save'))

    def load(self, tups):
        self.applyMethod('load', tups, bcast=True)
