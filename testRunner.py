#!/usr/bin/env python
from testdebug import TestRunner

from pyphase.tests import *

if __name__ == '__main__':
    testRunner = TestRunner(varsDict=vars(), localsDict=locals(), disableCleanUpInt=True)
    testRunner.getTestCases(exportToLocals=True)
    testRunner.main()
