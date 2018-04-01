# -*- coding: utf-8 -*-

import urwid


class SimpleButton(urwid.Button):

    def __init__(self, label, on_press=None, user_data=None, left_char='[', right_char=']'):
        self.button_left = urwid.Text(left_char)
        self.button_right = urwid.Text(right_char)
        super().__init__(label, on_press=on_press, user_data=user_data)


class WidgetButton(urwid.WidgetWrap):

    def __init__(self, widget, on_press=None, user_data=None, icon_char='*', delimiter='-', left_char='[', right_char=']'):

        self._user_data = user_data

        columns = [
            ('fixed', 2, urwid.Text(left_char)),
            ('fixed', 1, urwid.SelectableIcon(icon_char, cursor_position=0)),
            urwid.AttrMap(urwid.Padding(widget), None, focus_map='inverted'),
            ('fixed', 2, urwid.Text(right_char, align='right')),
        ]

        if delimiter:
            columns.insert(2, ('fixed', len(delimiter), urwid.Text(delimiter)))

        columns_widget = urwid.Columns(columns)
        self.__super.__init__(columns_widget)

        if on_press is not None:
            urwid.connect_signal(self, 'click', on_press)

    def keypress(self, size, key):
        if key != 'enter':
            return key

        urwid.emit_signal(self, 'click', self, self._user_data)


urwid.register_signal(WidgetButton, {'click'})


class SimpleMenu(urwid.WidgetWrap):

    def __init__(self, title, items, choice_callback=None):
        """
        :param str title:
        :param list[str] items:
        """

        body = urwid.ListBox(urwid.SimpleFocusListWalker([]))

        for item in items:
            button = SimpleButton(item, on_press=choice_callback, user_data=item)
            body.body.append(urwid.AttrMap(button, None, focus_map='inverted'))

        header = urwid.Pile([
            urwid.AttrMap(urwid.Text(title), 'inverted'),
            urwid.Divider(),
        ])

        super().__init__(urwid.Frame(body, header=header, footer=urwid.Divider()))
