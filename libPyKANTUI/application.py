# -*- coding: utf-8 -*-

import urwid

from .widgets import MainFrame
from .adapters import PyKanService


class Application(object):

    def __init__(self, pykan, palette):
        self.pykan = pykan
        """:type: PyKanService"""

        self._tui_ready = False

        self.main = MainFrame(self)
        """:type: MainFrame"""

        self.loop = urwid.MainLoop(urwid.LineBox(self.main), palette=palette)
        """:type: urwid.MainLoop"""

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
