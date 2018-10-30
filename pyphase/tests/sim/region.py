import numpy as np
from testdebug import Asserter, TestBase

from pyphase import LaneRegion

__all__ = ['LaneRegion_EqualN_TestBase']

def theoreticalExpected(regionSav, probs):
    ns = [np.sum(landSav[0] for landSav in landscapeSav)
          for landscapeSav in regionSav]

    return [np.sum(landSav[0]*p for p,landSav in zip(probs, landscapeSav))/n
            for n,landscapeSav in zip(ns, regionSav)]

def theoreticalSampleMean(regionSav):
    return [(arr[0] - arr[1])/arr[0] for arr in
            (np.sum(np.array(landSav) for landSav in landscapeSav)
             for landscapeSav in regionSav)]

class LaneRegion_Test(Asserter):
    def test_pebbleCount(self):
        for subn in self.laneRegion.n:
            self.assertEqual(self.n, subn)

        self.assertEqual(0, len(self.laneRegion.landscapeTerm.pebbles))

    def test_expected(self):
        intended = self.intended['expected']
        actual = self.laneRegionReloaded.expected()

        self.assertArrayAlmostEqual(intended, actual)

    def test_expected_theoretical(self):
        intended = theoreticalExpected(self.laneRegionSave, self.probs)
        actual = self.laneRegionReloaded.expected()

        self.assertArrayAlmostEqual(intended, actual)

    def test_sampleMean(self):
        intended = self.intended['sampleMean']
        actual = self.laneRegionReloaded.sampleMean()

        self.assertArrayAlmostEqual(intended, actual)

    def test_sampleMean_theoretical(self):
        intended = theoreticalSampleMean(self.laneRegionSave)
        actual = self.laneRegionReloaded.sampleMean()

        self.assertArrayAlmostEqual(intended, actual)

    def test_sampleVar(self):
        intended = self.intended['sampleVar']
        actual = self.laneRegionReloaded.sampleVar()

        self.assertArrayAlmostEqual(intended, actual)

    def test_var(self):
        intended = self.intended['var']
        actual = self.laneRegionReloaded.var()

        self.assertArrayAlmostEqual(intended, actual)

    def test_var_max(self):
        intended = self.intended['var_max']
        actual = self.laneRegionReloaded.var(max=True)

        self.assertArrayAlmostEqual(intended, actual)

        # turns out var and var_max are fundamentally equal
        intended = self.laneRegionReloaded.var()
        actual = self.laneRegionReloaded.var(max=True)

        self.assertArrayAlmostEqual(intended, actual)


class LaneRegion_EqualN_TestBase(TestBase, LaneRegion_Test):
    N = 4
    n = int(1e4)

    probs = [.1, .99]
    weights = [[.99, .01], [.01, .99]]

    laneRegion = None
    laneRegionSave = (
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

    @classmethod
    def genLaneRegion(cls):
        return LaneRegion(N=cls.N, probs=cls.probs, weights=cls.weights)

    @classmethod
    def setUpClass(cls):
        cls.laneRegion = cls.genLaneRegion()
        cls.laneRegion.run(cls.n)

        cls.laneRegionReloaded = cls.genLaneRegion()
        cls.laneRegionReloaded.load(*cls.laneRegionSave)
