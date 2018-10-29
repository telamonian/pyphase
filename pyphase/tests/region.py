from testdebug import TestBase

from pyphase import LaneRegion

__all__ = ['Test_LaneRegion_EqualN']

class Test_LaneRegion_EqualN(TestBase):
    n = int(1e4)
    laneRegion = None

    @classmethod
    def setUpClass(cls):
        cls.laneRegion = LaneRegion(nland=5, probs=[.1, .99], weights=[[.99, .01], [.01, .99]])
        cls.laneRegion.run(cls.n)

    def test_pebbleCount(self):
        for landscape in self.laneRegion.landscapes[:-1]:
            self.assertEqual(self.n, len(landscape.pebbles))

        self.assertEqual(0, len(self.laneRegion.landscapes[-1].pebbles))
