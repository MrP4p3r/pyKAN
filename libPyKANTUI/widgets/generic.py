# -*- coding: utf-8 -*-

import urwid


class SimpleButton(urwid.Button):

    def __init__(self, label, on_press=None, user_data=None, left_char='[', right_char=']'):
        self.button_left = urwid.Text(left_char)
        self.button_right = urwid.Text(right_char)
        super().__init__(label, on_press, user_data)


class WidgetButton(urwid.WidgetWrap):

    def __init__(self, widget, icon_char='*', delimiter='-', left_char='[', right_char=']'):

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
