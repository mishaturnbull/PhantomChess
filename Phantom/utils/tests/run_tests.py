#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)

"""Run all the tests in the Phantom.tests"""

from Phantom.utils.debug import log_msg, clear_log
import os
import inspect

def main(*args):
    clear_log()
    log_msg('Phantom beginning self-test', 0, mark=True)
    testdir = inspect.getfile(main)
    testdir, dirname = os.path.split(testdir)

    for f in os.listdir(testdir):
        if f in (dirname, '__init__.py'):
            continue
        else:
            mn = f[:f.index('.')]
            m = __import__(mn)
            m.main(False)
    log_msg('Phantom self-test complete', 0, mark=True)

if __name__ == '__main__':
    main()
