# -*- coding: utf-8 -*-

import urwid


class TabularList(urwid.WidgetWrap):

    def __init__(self, header, row_factory, data=None):
        data = data or []

        self._row_factory = row_factory

        self._list = urwid.SimpleFocusListWalker([])

        widget = urwid.Frame(urwid.ListBox(self._list), header=header)
        super().__init__(widget)

        self.extend(data)

    def append(self, item):
        self.extend([item])

    def extend(self, data):
        self._list.extend([self._row_factory(item) for item in data])

    def clear(self):
        self._list.clear()

    def set_focus(self, position):
        self._list.set_focus(position)
