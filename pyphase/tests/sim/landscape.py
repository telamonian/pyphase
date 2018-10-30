from testdebug import TestBase

from pyphase import Land, Landscape

__all__ = [] #'Landscape_TestBase']

class Landscape_TestBase(TestBase):
    N = 4
    n = int(1e2)

    probs = [.1, .99]
    weights = [[.99, .01], [.01, .99]]

    @classmethod
    def setUpClass(cls):
        pslow = cls.probs[0]
        pfast = cls.probs[1]
        pterm = 0

        wfast = cls.weights[1]
        wslow = cls.weights[0]
        wterm = [1.0]

        lscapeB = Landscape(name='B',
            lands=[Land('Bterm', pterm)],
            term=True)

        lscape2 = Landscape(name='2',
            lands=[Land('2slow', pslow, lscapeB, wterm),
                   Land('2fast', pfast, lscapeB, wterm)
                   ])

        lscape1 = Landscape(name='1',
            lands=[Land('1slow', pslow, lscape2, wslow),
                   Land('1fast', pfast, lscape2, wfast)
                   ])

        lscape0 = Landscape(name='0',
            lands=[Land('0slow', pslow, lscape1, wslow),
                   Land('0fast', pfast, lscape1, wfast)
                   ])

        lscapeA = Landscape(name='A',
            lands=[Land('Aslow', pslow, lscape0, wslow)])

        lscapeA.initPebbles(n)
        lscapeA.run()

        cls.landscapes = [lscapeA, lscape0, lscape1, lscape2, lscapeB]
