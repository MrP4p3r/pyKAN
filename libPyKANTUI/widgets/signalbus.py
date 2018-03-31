# -*- coding: utf-8 -*-

import urwid


class _SignalBus(urwid.Widget):

    def __init__(self):
        self._some_signals = set()

    def subscribe(self, signal_name, callback):
        self._ensure_signal_registered(signal_name)
        urwid.connect_signal(self, signal_name, callback)

    def send(self, signal_name, *args):
        urwid.emit_signal(self, signal_name, *args)

    def _ensure_signal_registered(self, signal_name):
        if signal_name not in self._some_signals:
            self._some_signals.add(signal_name)
            urwid.register_signal(self.__class__, self._some_signals)


_signal_bus = _SignalBus()

subscribe = _signal_bus.subscribe
send = _signal_bus.send
