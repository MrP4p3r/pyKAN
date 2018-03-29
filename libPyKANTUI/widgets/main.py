# -*- coding: utf-8 -*-

import urwid
import panwid


def menu_list(title, items, repr_fn=str, choice_callback=None):
    body = [urwid.AttrMap(urwid.Text(title), 'inverted'), urwid.Divider()]

    for item in items:
        menu_item = urwid.Button(repr_fn(item))
        if callable(choice_callback):
            urwid.connect_signal(menu_item, 'click', choice_callback, user_args=[menu_item, item])
        row = urwid.AttrMap(menu_item, None, focus_map='inverted')
        body.append(row)

    return urwid.Pile(urwid.SimpleFocusListWalker(body))


class ModsTable(panwid.datatable.DataTable):

    def __init__(self, mods):
        # _label = lambda name: urwid.AttrMap(urwid.Text(name), 'shaded')
        _label = lambda name, align='left': urwid.Text(name, align=align)
        columns = [
            panwid.datatable.DataTableColumn('status', label=_label('S', align='center'), width=3, align='center', format_fn=lambda s: s[0]),
            panwid.datatable.DataTableColumn('version', label=_label('Ver'), width=20),
            panwid.datatable.DataTableColumn('name', label=_label('Name')),
        ]

        data = list(map(lambda m: m.to_dict(), mods))

        super().__init__(columns=columns, data=data, index='identifier', sort_by='name', cell_selection=True)

    def query(self, sort=None, offset=None, **kwargs):
        return []

    @classmethod
    def create_wrapped(cls, mods, title, choice_callback=None):
        table = cls(mods)
        return urwid.BoxAdapter(urwid.Frame(table, header=urwid.Pile([urwid.AttrMap(urwid.Text(title), 'inverted')])), height=20)


class MainFrame(urwid.Frame):

    def __init__(self, app):
        self.app = app
        self._status_bar = urwid.Text('Nothing to show...')

        super().__init__(
            urwid.Filler(urwid.Text('Loading', align='center'), valign='middle'),
            footer=urwid.AttrMap(self._status_bar, 'inverted')
        )

        self.set_body(ModsListMenu(self.app))

    def set_status(self, markup):
        self._status_bar.set_text(markup)

    def keypress(self, size, key):
        if key == 'q':
            raise urwid.ExitMainLoop('Quit')
        return super().keypress(size, key)


class ModsListMenu(urwid.Filler):

    def __init__(self, app):
        """
        :param Application app:
        """

        self.app = app

        self._sections_widget = urwid.WidgetWrap(menu_list('Sections', ['All', 'Installed'], choice_callback=self.on_section_select))
        self._mods_widget = urwid.WidgetWrap(urwid.Widget())

        super().__init__(
            urwid.Columns([
                ('weight', 3, self._sections_widget),
                ('weight', 9, self._mods_widget),
            ], dividechars=1, focus_column=0), valign='top',
        )

        self.update_mods_list([])

    def on_section_select(self, loop, section, menu_item):
        self.app.main.set_status(f'Section {section} was selected')
        if section == 'Installed':
            installed_mods = self.app.pykan.list_installed()
            self.update_mods_list(installed_mods)
        else:
            self.update_mods_list([])

    def on_mod_select(self, loop, mod, menu_item):
        """
        :param loop:
        :param Mod mod:
        :return:
        """
        self.app.main.set_status(f'Mod {mod} was selected')

    def update_mods_list(self, mods):
        # self._mods_widget._set_w(menu_list('Mods', mods, choice_callback=self.on_mod_select))
        self._mods_widget._set_w(ModsTable.create_wrapped(mods, 'Mods'))
