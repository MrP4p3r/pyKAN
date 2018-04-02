# -*- coding: utf-8 -*-

import urwid

from .widgets import MainFrame
from .adapters import PyKanService


class Application(object):

    def __init__(self, pykan, palette):
        self.pykan = pykan
        """:type: PyKanService"""

        self._tui_ready = False

        placeholder = urwid.WidgetWrap(urwid.Filler(urwid.Text('Starting...', align='center')))
        self.loop = urwid.MainLoop(placeholder, palette=palette)
        """:type: urwid.MainLoop"""

        self.main = MainFrame(self)
        """:type: MainFrame"""

        actual_widget = urwid.LineBox(self.main)
        placeholder._set_w(actual_widget)

    def start(self):
        self.loop.run()


def init_app():
    pykan = PyKanService()

    palette = [
        ('inverted', 'standout', ''),
        ('shaded', '', 'dark gray'),
    ]

    app = Application(pykan, palette)
    return app
