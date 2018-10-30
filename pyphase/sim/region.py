import numpy as np

from ..applicator import Applicator
from .land import Land
from .landscape import Landscape

__all__ = ['LaneRegion']

class Region(Applicator):
    @property
    def _iterable(self):
        return self.landscapes

    @property
    def landscapes(self):
        return self._landscapes[:-1]

    @property
    def landscapeTerm(self):
        return self._landscapes[-1]

    @property
    def expected(self):
        return self.aget('expected')

    @property
    def expectedDivN(self):
        return self.expected*(1/self.nmat)

    @property
    def n(self):
        return self.aget('n')

    @property
    def nmat(self):
        nsqrt = np.sqrt(self.aget('n', array=True).reshape(-1, 1))
        return nsqrt.dot(nsqrt.T)

    def __init__(self, N, *args, **kwargs):
        self.N = N
        self._landscapes = None

        self.init(*args, **kwargs)

    def init(self, *args, **kwargs):
        pass

    def run(self, *ns):
        if len(ns)==1:
            ns = ns*self.N
        elif len(ns) != self.N:
            raise ValueError

        self.landscapes[0].initPebbles(ns[0])
        self.landscapes[0].run()

        for prevl,l,n in zip(self.landscapes[:-1], self.landscapes[1:], ns[1:]):
            prevl.setNextPebbleSample(n)
            l.run()

    def save(self):
        return tuple(sav for sav in self.applyMethod('save'))

    def load(self, *landscapeSav):
        self.applyMethod('load', *landscapeSav, bcast=True)

class LaneRegion(Region):
    _pterm = 0
    _wterm = [1.0]

    def init(self, probs, weights):
        if self.N < 2:
            raise ValueError

        if len(probs) != len(weights):
            raise ValueError

        self.laneProbs = probs
        self.laneWeights = weights
        self.laneCount = len(probs)

        # terminal landscape is defined first
        self._landscapes = [Landscape(
            name='B',
            lands=[Land('Bterm', self._pterm)],
            term=True
        )]

        # the intermediate landscapes that make up the lanes
        for i in reversed(range(self.N - 1)):
            name = '%d' % i
            self._landscapes.insert(0, Landscape(
                name=name,
                lands=self.genLaneLands(name, self._landscapes[0])
            ))

        # initial landscape
        self._landscapes.insert(0, Landscape(
            name='A',
            lands=[Land('Astart', self.laneProbs[0], self._landscapes[0], self.laneWeights[0])]
        ))

    def genLaneLands(self, name, nextLandscape):
        if nextLandscape.term:
            # if the next landscape is the last, there's only one land everything is going to end up in
            laneWeights = [[1]]*len(self.laneProbs)
        else:
            laneWeights = self.laneWeights

        return [Land('%s%d' % (name, i), p, nextLandscape, w)
                for i,(p,w) in enumerate(zip(self.laneProbs, laneWeights))]
