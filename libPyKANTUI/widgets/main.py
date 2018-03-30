# -*- coding: utf-8 -*-

import urwid

from . import generic


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
        urwid.connect_signal(mods_menu, 'on_section_select', self.on_section_select)

        self.set_body(mods_menu)

    def set_status(self, markup):
        self._status_bar.set_text(markup)

    def keypress(self, size, key):
        if key == 'q':
            raise urwid.ExitMainLoop('Quit')
        return super().keypress(size, key)

    def on_section_select(self, mods_list, section_name):
        self.set_status(f'Section {section_name} was selected.')

        if section_name == 'Installed':
            mods = self.app.pykan.list_installed()
            mods_list.set_mods(mods)
        else:
            mods_list.set_mods([])


class ModsMenu(urwid.WidgetWrap):

    def __init__(self, app):
        self.app = app

        self._mods_list = ModsList()

        super().__init__(
            urwid.Columns([
                (30, generic.SimpleMenu('Sections', ['All', 'Installed'], choice_callback=self.section_selected)),
                self._mods_list,
            ], dividechars=1)
        )

    def section_selected(self, loop, section_name):
        urwid.emit_signal(self, 'on_section_select', self._mods_list, section_name)


urwid.register_signal(ModsMenu, 'on_section_select')


class ModsList(urwid.WidgetWrap):

    def __init__(self):

        table_header = urwid.Padding(
            urwid.Columns([
                (3, urwid.Padding(urwid.Text('S'), width=3)),
                (20, urwid.Text('Version')),
                urwid.Text('Name')
            ]),
            left=2, right=2
        )

        header = urwid.Pile([
            urwid.AttrMap(urwid.Text('Mods'), 'inverted'),
            # urwid.Divider(),
            table_header,
        ])

        body = urwid.ListBox(urwid.SimpleFocusListWalker([]))

        super().__init__(urwid.Frame(body, header=header, footer=urwid.Divider()))

    def set_mods(self, mods):
        w = self._wrapped_widget.body.body
        """:type: urwid.SimpleFocusListWalker"""

        mod_rows = [
            generic.WidgetButton(
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
            for mod in mods
        ]

        w.clear()
        w.extend(mod_rows)
