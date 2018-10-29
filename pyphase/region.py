from .land import Land
from .landscape import Landscape

__all__ = ['LaneRegion']

class Region:
    def __init__(self, *args, **kwargs):
        self.landscapes = None

        self.init(*args, **kwargs)

    def init(self, *args, **kwargs):
        pass

    def run(self, *ns):
        nlandscapes = len(self.landscapes)
        if len(ns)==1:
            ns = ns*nlandscapes
        elif len(ns) != nlandscapes:
            raise ValueError

        self.landscapes[0].initPebbles(ns[0])
        self.landscapes[0].run()

        for prevl,l,n in zip(self.landscapes[:-2], self.landscapes[1:-1], ns[1:]):
            prevl.setNextPebbleSample(n)
            l.run()

class LaneRegion(Region):
    _pterm = 0
    _wterm = [1.0]

    def init(self, nland, probs, weights):
        if nland < 3:
            raise ValueError

        if len(probs) != len(weights):
            raise ValueError

        self.laneProbs = probs
        self.laneWeights = weights
        self.laneCount = len(probs)

        # terminal landscape is defined first
        self.landscapes = [Landscape(
            name='B',
            lands=[Land('Bterm', self._pterm)],
            term=True
        )]

        # the intermediate landscapes that make up the lanes
        for i in reversed(range(nland - 2)):
            name = '%d' % i
            self.landscapes.insert(0, Landscape(
                name=name,
                lands=self.genLaneLands(name, self.landscapes[0])
            ))

        # initial landscape
        self.landscapes.insert(0, Landscape(
            name='A',
            lands=[Land('Astart', self.laneProbs[0], self.landscapes[0], self.laneWeights[0])]
        ))

    def genLaneLands(self, name, nextLandscape):
        if nextLandscape.term:
            # if the next landscape is the last, there's only one land everything is going to end up in
            laneWeights = [[1]]*len(self.laneProbs)
        else:
            laneWeights = self.laneWeights

        return [Land('%s%d' % (name, i), p, nextLandscape, w)
                for i,(p,w) in enumerate(zip(self.laneProbs, laneWeights))]
