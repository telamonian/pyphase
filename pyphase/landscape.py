from numpy import random as rnd

__all__ = ['Applicator', 'Landscape']

class Applicator:
    @property
    def _iterable(self):
        """Any subclass will need to override this property with
        something that actually returns an iterable
        """
        pass

    def apply(self, func, *args, **kwargs):
        return [func(obj, *args, **kwargs) for obj in self._iterable]

    def aGet(self, attr):
        return self.apply(getattr, attr)

    def aGetFlat(self, attr):
        flat = []
        for sub in self.aGet(attr):
            flat.extend(sub)
        return flat

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
    def pebbles(self):
        return self.aGetFlat('pebbles')

    @property
    def failedPebbles(self):
        return self.aGetFlat('failedPebbles')

    @property
    def successfulPebbles(self):
        return self.aGetFlat('successfulPebbles')

    def run(self, nsample=None, auto=True):
        if self.term:
            return

        self.n = 0
        for l in self.lands:
            self.n += l.run()

        self.setPebbleSample(n=nsample)
        if auto:
            for endscape in self.endscapes:
                endscape.run(nsample=nsample)

    def chooseLands(self, n, p=None):
        if not self.lands:
            raise ValueError("self.lands is empty")

        return rnd.choice(self.lands, size=n, p=p)

    def initPebbles(self, *n):
        for l,nl in zip(self.lands, n):
            l.initPebbles(n=nl)

    def setPebbleSample(self, n=None):
        n = self.n if n is None else n

        # choose a sample of appropriate size
        self.pebbleSample = rnd.choice(self.successfulPebbles, size=n)
        for p in self.pebbleSample:
            p.land.addNewPebble(p.copy())

        # assign each of the sampled pebbles to its current land
        for land in self.endlands:
            land.setNewPebbles()

    def pebbleStats(self):
        stats = {}
        stats['p'] = len(self.successfulPebbles)/len(self.pebbles)

        return stats
