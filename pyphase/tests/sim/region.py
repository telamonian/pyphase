import numpy as np
from testdebug import Asserter, TestBase

from pyphase import LaneRegion

__all__ = ['LaneRegion_EqualN_TestBase']

class LaneRegion_Test(Asserter):
    def test_pebbleCount(self):
        for subn in self.laneRegion.n:
            self.assertEqual(self.n, subn)

        self.assertEqual(0, len(self.laneRegion.landscapeTerm.pebbles))

    def test_expected(self):
        intended = [0.1006,0.1066,0.1975,0.579]
        actual = self.laneRegionReloaded.expected

        self.assertArrayAlmostEqual(intended, actual)

    def test_expected_theoretical(self):
        intended = [(arr[0] - arr[1])/arr[0] for arr in
                    (np.sum(np.array(landSav) for landSav in landscapeSav)
                     for landscapeSav in self.laneRegionSave)]
        actual = self.laneRegionReloaded.expected

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

    @classmethod
    def genLaneRegion(cls):
        return LaneRegion(N=cls.N, probs=cls.probs, weights=cls.weights)

    @classmethod
    def setUpClass(cls):
        cls.laneRegion = cls.genLaneRegion()
        cls.laneRegion.run(cls.n)

        cls.laneRegionReloaded = cls.genLaneRegion()
        cls.laneRegionReloaded.load(*cls.laneRegionSave)
