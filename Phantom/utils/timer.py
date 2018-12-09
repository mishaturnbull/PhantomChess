# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)

"""Game timer.
Similar in use to `timeit.timeit()`, but is much more flexible and (I find) easier to use."""

import time
from Phantom.core.chessobj import PhantomObj

class Timer (PhantomObj):

    def __init__(self, active=True):
        self.is_active = active
        self.init_time = time.time()
        self.start_time = self.init_time
        self.stopped_total = 0
        self.stop_time = self.init_time
        self.pause_time = self.init_time if not active else None
        self.resume_time = None

    def start(self):
        self.is_active = True
        self.start_time = time.time()

    def stop(self):
        self.is_active = False
        self.stop_time = time.time()

    def pause(self):
        self.pause_time = time.time()
        self.is_active = False

    def resume(self):
        self.resume_time = time.time()
        self.is_active = True
        self.stopped_total += self.resume_time - self.pause_time
        self.pause_time = self.resume_time = None

    def get_total(self):
        return (self.stop_time or time.time()) - self.start_time

    def get_run(self):
        totaltime = self.get_total()
        return totaltime - self.stopped_total
