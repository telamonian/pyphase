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

    def test_expectedEstimator(self):
        intended = self.intended['expectedEstimator']
        actual = self.simReloaded.expectedEstimator()

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
            [3.81295e-32,-8.08891e-33,-9.81252e-33,2.36092e-32],
            [-8.08891e-33,7.69823e-06,6.28392e-05,0.000184966],
            [-9.81252e-33,6.28392e-05,0.000531458,0.00156291],
            [2.36092e-32,0.000184966,0.00156291,0.00475734],
        ]),
        ('expectedEstimator', [0.1,0.10892,0.187724,0.553736]),
        ('sampleMean',        [0.099492,0.109322,0.188192,0.55377]),
        ('sampleVar',         [0.0895857,0.0973573,0.152265,0.242385]),
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
