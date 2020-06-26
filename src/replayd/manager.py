# -*- coding: utf-8 -*-
import time

class Manager:

    def __init__(self, sourcer, sinker, loop=1, interval=0):
        self._sourcer = sourcer
        self._sinker = sinker
        self._loop = int(loop)
        self._interval = float(interval)

    def run(self):
        if self._loop > 0:
            for i in range(self._loop):
                self._run(version=i)
                if i < self._loop - 1:
                    time.sleep(self._interval)
        else:
            i = 0
            while True:
                self._run(version=i)
                i += 1
                time.sleep(self._interval)

    def _run(self, version=0):
        for data in self._sourcer.draw(version=version):
            self._sinker.export(data)
