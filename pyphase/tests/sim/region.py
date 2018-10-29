from testdebug import Asserter, TestBase

from pyphase import LaneRegion

__all__ = ['LaneRegion_EqualN_TestBase']

class LaneRegion_Test(Asserter):
    def test_pebbleCount(self):
        for landscape in self.laneRegion.landscapes[:-1]:
            self.assertEqual(self.n, len(landscape.pebbles))

        self.assertEqual(0, len(self.laneRegion.landscapes[-1].pebbles))

class LaneRegion_EqualN_TestBase(TestBase, LaneRegion_Test):
    N = 4
    n = int(1e2)

    probs = [.1, .99]
    weights = [[.99, .01], [.01, .99]]

    laneRegion = None

    @classmethod
    def setUpClass(cls):
        cls.laneRegion = LaneRegion(N=cls.N, probs=cls.probs, weights=cls.weights)
        cls.laneRegion.run(cls.n)
