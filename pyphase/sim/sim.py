import numpy as np

from .region import Region, LaneRegion
from ..applicator import Applicator

__all__ = ['Sim', 'LaneSim']

def _summarize(arr, summary):
    if summary:
        return np.mean(arr, axis=0)
    else:
        return arr.T

class Sim(Applicator):
    regionType = Region

    @property
    def _iterable(self):
        return self.regions

    def __init__(self, reps, N, *args, **kwargs):
        self.reps = reps

        self.regions = self.genRegions(N, *args, **kwargs)

    def genRegions(self, N, *args, **kwargs):
        return [self.regionType(N, *args, **kwargs) for i in range(self.reps)]

    def run(self, *ns):
        self.applyMethod('run', *ns)

    def save(self):
        return tuple(sav for sav in self.applyMethod('save'))

    def load(self, *regionSav):
        self.applyMethod('load', *regionSav, bcast=True)


    def covEstimator(self):
        return np.cov(self.expectedEstimator(summary=False))

    def expectedEstimator(self, summary=True):
        kwargs = {'summary': summary, 'transpose': not summary}
        return self.applyMethod('expected', **kwargs)

    def sampleMean(self, summary=True):
        kwargs = {'summary': summary, 'transpose': not summary}
        return self.applyMethod('sampleMean', **kwargs)

    def sampleVar(self, ddof=0, summary=True):
        kwargs = {'summary': summary, 'transpose': not summary}
        return self.applyMethod('sampleVar', ddof=ddof, **kwargs)

class LaneSim(Sim):
    regionType = LaneRegion
