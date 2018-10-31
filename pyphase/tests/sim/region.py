import numpy as np
from testdebug import Asserter, TestBase

from pyphase import LaneRegion

__all__ = ['LaneRegion_EqualN_TestBase', 'LaneRegion_TestBase']

def theoreticalExpected(regionSav, probs):
    ns = [np.sum(landSav[0] for landSav in landscapeSav)
          for landscapeSav in regionSav]

    return [np.sum(landSav[0]*p for p,landSav in zip(probs, landscapeSav))/n
            for n,landscapeSav in zip(ns, regionSav)]

def theoreticalSampleMean(regionSav):
    return [(arr[0] - arr[1])/arr[0] for arr in
            (np.sum(np.array(landSav) for landSav in landscapeSav)
             for landscapeSav in regionSav)]

class _Region_Test(Asserter):
    N = None
    n = None

    probs = None
    weights = None

    region = None
    regionReloaded = None
    regionSave = None

    intended = None

    def test_pebbleCount(self):
        for subn in self.region.n:
            self.assertEqual(self.n, subn)

        self.assertEqual(0, len(self.region.landscapeTerm.pebbles))

    def test_expected(self):
        intended = self.intended['expected']
        actual = self.regionReloaded.expected()

        self.assertArrayAlmostEqual(intended, actual)

    def test_expected_theoretical(self):
        intended = theoreticalExpected(self.regionSave, self.probs)
        actual = self.regionReloaded.expected()

        self.assertArrayAlmostEqual(intended, actual)

    def test_sampleMean(self):
        intended = self.intended['sampleMean']
        actual = self.regionReloaded.sampleMean()

        self.assertArrayAlmostEqual(intended, actual)

    def test_sampleMean_theoretical(self):
        intended = theoreticalSampleMean(self.regionSave)
        actual = self.regionReloaded.sampleMean()

        self.assertArrayAlmostEqual(intended, actual)

    def test_sampleVar(self):
        intended = self.intended['sampleVar']
        actual = self.regionReloaded.sampleVar()

        self.assertArrayAlmostEqual(intended, actual)

    def test_var(self):
        intended = self.intended['var']
        actual = self.regionReloaded.var()

        self.assertArrayAlmostEqual(intended, actual)

    def test_var_max(self):
        intended = self.intended['var_max']
        actual = self.regionReloaded.var(max=True)

        self.assertArrayAlmostEqual(intended, actual)

        # turns out var and var_max are fundamentally equal
        intended = self.regionReloaded.var()
        actual = self.regionReloaded.var(max=True)

        self.assertArrayAlmostEqual(intended, actual)


class _LaneRegion_Test(TestBase, _Region_Test):
    @classmethod
    def genLaneRegion(cls):
        return LaneRegion(N=cls.N, probs=cls.probs, weights=cls.weights)

    @classmethod
    def setUpClass(cls):
        cls.region = cls.genLaneRegion()
        cls.region.run(*cls.n)

        cls.regionReloaded = cls.genLaneRegion()
        cls.regionReloaded.load(*cls.regionSave)

class LaneRegion_EqualN_TestBase(_LaneRegion_Test):
    N = 4
    n = [int(1e4)]

    probs = [.1, .99]
    weights = [[.99, .01], [.01, .99]]

    regionSave = (
        ((10000, 8994),),
        ((9906, 8934), (94, 0)),
        ((8927, 8018), (1073, 7)),
        ((4614, 4159), (5386, 51))
    )

    intended = dict([
        ('expected',   [0.1,0.108366,0.195497,0.579354]),
        ('sampleMean', [0.1006,0.1066,0.1975,0.579]),
        ('sampleVar',  [0.0904796,0.0952364,0.158494,0.243759]),
        ('var',        [0.09,0.0966228,0.157278,0.243703]),
        ('var_max',    [0.09,0.0966228,0.157278,0.243703]),
    ])

class LaneRegion_TestBase(_LaneRegion_Test):
    N = 4
    n = [int(5e3), int(1e4), int(1.5e4), int(9e3)]

    probs = [.1, .99]
    weights = [[.99, .01], [.01, .99]]

    regionSave = (
        ((5000, 4478),),
        ((9877, 8851), (123, 3)),
        ((13364, 11989), (1636, 17)),
        ((4146, 3723), (4854, 51))
    )

    intended = dict([
        ('expected',   [0.1,0.110947,0.197069,0.580007]),
        ('sampleMean', [0.1044,0.1146,0.1996,0.580667]),
        ('sampleVar',  [0.0935006,0.101467,0.15976,0.243493]),
        ('var',        [0.09,0.0986378,0.158233,0.243599]),
        ('var_max',    [0.09,0.0986378,0.158233,0.243599]),
    ])
