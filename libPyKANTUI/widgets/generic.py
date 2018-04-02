# -*- coding: utf-8 -*-

import urwid


def with_signals(signal_names):
    def registar(cls):
        urwid.register_signal(cls, signal_names)
        return cls
    return registar


class TextButton(urwid.Button):

    def __init__(self, label, on_press=None, user_data=None, left_char='[', right_char=']'):
        self.button_left = urwid.Text(left_char)
        self.button_right = urwid.Text(right_char)
        super().__init__(label, on_press=on_press, user_data=user_data)


@with_signals({'click'})
class WidgetButton(urwid.WidgetWrap):

    def __init__(self, widget, on_press, user_data=None, icon_char='*', left_char='[', right_char=']'):

        self._user_data = user_data
        self._left_char = urwid.Text(left_char)
        self._icon = urwid.SelectableIcon(icon_char, cursor_position=0)
        self._right_char = urwid.Text(right_char, align='right')

        columns = [
            ('fixed', 2, self._left_char),
            ('fixed', 2, self._icon),
            widget,
            ('fixed', 2, self._right_char)
        ]

        packed_columns = urwid.Columns(columns)
        super().__init__(packed_columns)

        if on_press is not None:
            urwid.connect_signal(self, 'click', on_press)

    def keypress(self, size, key):
        if key != 'enter':
            return key

        urwid.emit_signal(self, 'click', self, self._user_data)


class ItemListFrame(urwid.WidgetWrap):

    def __init__(self, header, footer, row_factory, data=None):
        data = data or []
        self._row_factory = row_factory
        self._list = urwid.SimpleFocusListWalker([])

        self._frame_widget = urwid.Frame(urwid.ListBox(self._list), header=header, footer=footer)
        super().__init__(self._frame_widget)

        self.extend(data)

        self.set_focus(0)

    def append(self, item):
        self.extend([item])

    def extend(self, data):
        self._list.extend([self._row_factory(item) for item in data])

    def clear(self):
        self._list.clear()

    def set_focus(self, position):
        self._list.set_focus(position)

    def focus_footer(self):
        self._frame_widget.set_focus('footer')

    def focus_body(self):
        self._frame_widget.set_focus('body')

    @classmethod
    def from_text_items(cls, title, items, on_press=None):
        """Simple factory to create menu from text items."""

        header = urwid.Pile([
            urwid.AttrMap(urwid.Text(title), 'inverted'),
            urwid.Divider(),
        ])

        footer = urwid.Divider()

        def row_factory(item):
            button = TextButton(item, on_press=on_press, user_data=item)
            widget = urwid.AttrMap(button, None, focus_map='inverted')
            return widget

        return cls(header, footer, row_factory, items)
