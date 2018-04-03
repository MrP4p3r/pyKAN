# -*- coding: utf-8 -*-

import urwid

from . import generic
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
        if super().keypress(size, key) is None:
            return
        if key == 'q':
            raise urwid.ExitMainLoop('Quit')
        return key


class ModsMenu(urwid.WidgetWrap):

    def __init__(self, app):
        self.app = app
        """:type: libPyKANTUI.application.Application"""

        self._mods_list = ModsList.create(on_press=self.on_mod_select)
        self._selected_section = 'All'
        self._mod_filters = {}

        super().__init__(
            urwid.Columns([
                (30, generic.ItemListFrame.from_text_items('Sections', ['All', 'Installed'], on_press=self.on_section_select)),
                self._mods_list,
            ], dividechars=1)
        )

        urwid.connect_signal(self._mods_list, 'search_text_update', self.on_search_text_update)
        # Hack to automatically select 'All'
        self.on_section_select(self.app.loop, 'All')

    def on_section_select(self, loop, section_name):
        signalbus.send('update_status', f'Section {section_name} was selected.')

        if section_name == 'Installed':
            self._mod_filters['status'] = 'installed'
        elif section_name == 'All':
            self._mod_filters.clear()
        else:
            raise KeyError('Unknown section')

        self._selected_section = section_name

        self.update_mod_list()

    def on_mod_select(self, button, mod):
        signalbus.send('update_status', f'Mod {mod.name} was selected')

    def on_search_text_update(self, text):
        signalbus.send('update_status', f'Searching: {text}')
        self._mod_filters['fuzzyfindtext'] = text
        self.update_mod_list()

    def update_mod_list(self):
        mods = self.app.pykan.mods.find(self._mod_filters)
        self._mods_list.clear()
        if mods:
            self._mods_list.extend(mods)
            self._mods_list.set_focus(0)


urwid.register_signal(ModsMenu, {'status_update'})


@generic.with_signals({'search_text_update'})
class ModsList(generic.ItemListFrame):

    @classmethod
    def create(cls, mods=None, on_press=None):
        """
        :param list[libPyKANTUI.models.Mod] mods:
        :param callable on_press:
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
            """Creates mod representation as button in ItemListFrame.

            :param libPyKANTUI.models.Mod mod:
            :return: Mod representation
            :rtype: urwid.Widget

            """

            row = generic.WidgetButton(
                urwid.Padding(
                    urwid.Columns([
                        (1, urwid.Divider()),
                        (20, urwid.Text(mod.version)),
                        urwid.Text(mod.name),
                    ]),
                    align='left'
                ),
                on_press=on_press,
                user_data=mod,
                icon_char=mod.status[0],
            )

            return row

        footer = search_edit = urwid.Edit()

        instance = cls(header, footer, row_factory=row_factory, data=mods)
        instance._search_edit = search_edit
        urwid.connect_signal(footer, 'change', instance.on_search_text_change)

        return instance

    def keypress(self, size, key):
        if super().keypress(size, key) is None:
            return

        if key == '/':
            self.focus_footer()
        elif key == 'esc':
            if self._frame_widget.focus_part == 'footer':
                self.focus_body()
                self._search_edit.set_edit_text('')
        elif key == 'enter':
            if self._frame_widget.focus_part == 'footer':
                self.focus_body()
        else:
            return key

    def on_search_text_change(self, widget_edit, text):
        urwid.emit_signal(self, 'search_text_update', text)
