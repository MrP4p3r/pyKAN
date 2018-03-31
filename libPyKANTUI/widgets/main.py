# -*- coding: utf-8 -*-

import urwid

from . import generic
from . import tabularlist
from . import signalbus


class MainFrame(urwid.Frame):

    def __init__(self, app):
        self.app = app
        """:type: libPyKANTUI.application.Application"""

        self._status_bar = urwid.Text('Nothing to show...')

        super().__init__(
            urwid.Filler(urwid.Text('Loading', align='center'), valign='middle'),
            footer=urwid.AttrMap(self._status_bar, 'inverted')
        )

        mods_menu = ModsMenu(self.app)
        signalbus.subscribe('update_status', self.set_status)

        self.set_body(mods_menu)

    def set_status(self, markup):
        self._status_bar.set_text(markup)

    def keypress(self, size, key):
        if key == 'q':
            raise urwid.ExitMainLoop('Quit')
        return super().keypress(size, key)


class ModsMenu(urwid.WidgetWrap):

    def __init__(self, app):
        self.app = app

        self._mods_list = ModsList.create()

        super().__init__(
            urwid.Columns([
                (30, generic.SimpleMenu('Sections', ['All', 'Installed'], choice_callback=self.on_section_select)),
                self._mods_list,
            ], dividechars=1)
        )

    def on_section_select(self, loop, section_name):
        signalbus.send('update_status', f'Section {section_name} was selected.')

        mods = None
        if section_name == 'Installed':
            mods = self.app.pykan.mods.list_installed()
        elif section_name == 'All':
            mods = self.app.pykan.mods.list_all()

        self._mods_list.clear()
        if mods:
            self._mods_list.extend(mods)
            self._mods_list.set_focus(0)


urwid.register_signal(ModsMenu, {'status_update'})


class ModsList(tabularlist.TabularList):

    @classmethod
    def create(cls, mods=None):
        """
        :param list[libPyKANTUI.models.Mod] mods:
        :rtype: ModsList
        """

        table_header = urwid.Padding(
            urwid.Columns([
                (3, urwid.Padding(urwid.Text('S'), width=3)),
                (20, urwid.Text('Version')),
                urwid.Text('Name')
            ]),
            left=2,
            right=2,
        )

        header = urwid.Pile([urwid.AttrMap(urwid.Text('Mods'), 'inverted'), table_header])

        def row_factory(mod):
            """
            :param libPyKANTUI.models.Mod mod:
            :return: Mod representation
            :rtype: urwid.Widget
            """
            row = generic.WidgetButton(
                urwid.Padding(
                    urwid.Columns([
                        (20, urwid.Text(mod.version)),
                        urwid.Text(mod.name),
                    ]),
                    align='left'
                ),
                icon_char=mod.status[0],
                delimiter='  '
            )

            return row

        return cls(header, row_factory=row_factory, data=mods)
