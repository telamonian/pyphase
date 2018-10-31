import numpy as np
from testdebug import Asserter, TestBase

from pyphase import LaneSim
from pyphase.tests.data.simSave import simSave_LaneSim_EqualN

__all__ = ['LaneSim_EqualN_TestBase']

class _Sim_Test(Asserter):
    reps = None
    N = None
    n = None

    probs = None
    weights = None

    sim = None
    simReloaded = None
    simSave = None

    intended = None

    def test_covEstimator(self):
        intended = self.intended['covEstimator']
        actual = self.simReloaded.covEstimator()

        self.assertArrayAlmostEqual(intended, actual)

    def test_expected(self):
        intended = self.intended['expected']
        actual = self.simReloaded.expected()

        self.assertArrayAlmostEqual(intended, actual)

    def test_sampleMean(self):
        intended = self.intended['sampleMean']
        actual = self.simReloaded.sampleMean()

        self.assertArrayAlmostEqual(intended, actual)

    def test_sampleVar(self):
        intended = self.intended['sampleVar']
        actual = self.simReloaded.sampleVar()

        self.assertArrayAlmostEqual(intended, actual)

class LaneSim_EqualN_TestBase(TestBase, _Sim_Test):
    _outputSimSave = False

    reps = 100
    N = 4
    n = [int(1e4)]

    probs = [.1, .99]
    weights = [[.99, .01], [.01, .99]]

    simSave = simSave_LaneSim_EqualN

    intended = dict([
        ('covEstimator', [
            [7.68539e-06,1.12523e-06,9.27559e-06,2.65175e-05],
            [1.12523e-06,1.35106e-05,4.88224e-05,0.000152594],
            [9.27559e-06,4.88224e-05,0.000515784,0.00151831],
            [2.65175e-05,0.000152594,0.00151831,0.00477142],
        ]),
        ('expected',   [0.1,0.10892,0.187724,0.553736]),
        ('sampleMean', [0.099492,0.109322,0.188192,0.55377]),
        ('sampleVar',  [0.0895857,0.0973573,0.152265,0.242385]),
    ])

    @classmethod
    def genLaneSim(cls):
        return LaneSim(reps=cls.reps, N=cls.N, probs=cls.probs, weights=cls.weights)

    @classmethod
    def setUpClass(cls):
        # if cls._outputSimSave:
        #     cls.sim = cls.genLaneSim()
        #     cls.sim.run(*cls.n)
        #     for tup in cls.sim.save():
        #         print(tup, ',', sep='')

        cls.simReloaded = cls.genLaneSim()
        cls.simReloaded.load(*cls.simSave)
