#!/usr/bin/env python
from testdebug import TestRunner

if __name__ == '__main__':
    testRunner = TestRunner(fullnameDefault='pyphase.tests')
    # testRunner.getTestCases(exportToLocals=True)
    testRunner.main()
