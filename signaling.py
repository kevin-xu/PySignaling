# The MIT License (MIT)
#
# Copyright (c) 2018 Kevin XU <kevin.xu.1982.02.06@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
#
#
# Author: Kevin XU <kevin.xu.1982.02.06@gmail.com>
#

class Signaling:
    @classmethod
    def __init_subclass__(klass, **kwargs):
        super().__init_subclass__(**kwargs)

        klass._signals_ = {}

    @classmethod
    def register(klass, signal, **signature):
        for key in signature:
            if not isinstance(signature[key], type):
                raise TypeError("")

        klass._signals_[signal] = signature

    def __init__(self):
        self._ms2si = {}
        self._ms2sis = {}
        self._ms2msi2s = {}

    def connect(self, signal, slot):
        if not signal in type(self)._signals_:
            raise ValueError("")

        if not callable(slot):
            raise TypeError("")

        if not signal in self._ms2msi2s:
            self._ms2msi2s[signal] = {}

        msi2s = self._ms2msi2s[signal]

        if signal in _ms2sis and self._ms2sis[signal]:
            subconnectionId = self._ms2sis[signal].pop(0)
        else:
            if not signal in self._ms2si:
                self._ms2si[signal] = 0

            subconnectionId = self._ms2si[signal], self._ms2si[signal] += 1

        msi2s[subconnectionId] = slot

        return (signal, subconnectionId)

    def disconnectById(self, connectionId):
        if not isinstance(connectionId, tuple):
            raise TypeError("")

        if len(connectionId) != 2 or not isinstance(connectionId[1], int):
            raise TypeError("")

        signal = connectionId[0]

        if not signal in type(self)._signals_:
            raise ValueError("")

        if not signal in self._ms2msi2s:
            return

        subconnectionId = connectionId[1]

        msi2s = self._ms2msi2s[signal]

        if not subconnectionId in msi2s:
            return

        msi2s.pop(subconnectionId)

        if not signal in self._ms2sis:
            self._ms2sis[signal] = []

        self._ms2sis[signal].append(subconnectionId)

    def disconnectSignal(self, signal):
        if not signal in type(self)._signals_:
            raise ValueError("")

        if signal in _ms2msi2s:
            _ms2msi2s[signal].clear()

        if signal in _ms2si:
            _ms2si[signal] = 0

        if signal in _ms2sis:
            _ms2sis[signal].clear()

    def disconnectAll(self):
        for signal in type(self)._signals_:
            self.disconnectSignal(signal)

    def emit(self, signal, **kwargs):
        klass = type(self)

        if not signal in klass._signals_:
            raise ValueError("")

        signature = klass._signals_[signal]

        for key in kwargs:
            if not key in signature:
                raise KeyError("")

            if not isinstance(kwargs[key], signature[key]):
                raise TypeError("")

        if not signal in self._ms2msi2s:
            return

        msi2s = self._ms2msi2s[signal]

        for si in msi2s:
            msi2s[si](**kwargs)

