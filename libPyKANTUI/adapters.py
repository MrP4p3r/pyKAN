# -*- coding: utf-8 -*-

import itertools

from libPyKAN import ckanRepo
from libPyKAN.pykancfg import PyKANSettings
from libPyKAN.installed import Installed

from .models import Mod


class PyKanService(object):
    """"""

    def __init__(self):
        self._kspdir = None
        self._settings = PyKANSettings(self._kspdir)

        self._repo = ckanRepo.CkanRepo(self._settings)
        self._installed = Installed(self._settings, self._repo)
        self._settings.reload()

        self.mods = PyKanMods(self._installed, self._repo)


class PyKanMods(object):
    """Adapter for mods related stuff via libPyKAN"""

    def __init__(self, installed, repo):
        """
        :param Installed installed:
        :param ckanRepo.CkanRepo repo:
        """
        self._installed = installed
        self._repo = repo

    def find(self, filters, limit=100):
        status = filters.get('status')
        fuzzyfindtext = filters.get('fuzzyfindtext')

        # *Filter* by status
        if status == 'installed':
            mod_list_it = Mod.from_dicts(self._installed.list_modules())
        else:
            mod_list_it = Mod.from_dicts(self._repo.list_modules())

        if fuzzyfindtext:
            mod_list_it = fuzzyfinder(fuzzyfindtext, mod_list_it, lambda mod: [mod.identifier, mod.name], limit=limit)

        # Limit
        mod_list_it = itertools.islice(mod_list_it, limit)

        # Make list and return
        return list(mod_list_it)


def fuzzyfinder(search_string, collection, accessor=lambda x: x, threshold=80, limit=100):
    """Slightly *modified* version of fuzzyfinder function from `fuzzyfinder` package.

    :param str search_string:
        A partial string which is typically entered by a user.

    :param iterable collection:
        A collection of strings which will be filtered based on the `input`.

    :param (T) -> (str or list[str]) accessor:
        If the `collection` is not an iterable of strings,
        then use the accessor to fetch the string *or list of strings* that
        will be used for fuzzy matching.

    :return:
        Suggestions (generator): A generator object that produces a list of
        suggestions narrowed down from `collection` using the `input`.

    :rtype: generator[T]

    """

    import re

    suggestions = []
    search_string = str(search_string) if not isinstance(search_string, str) else search_string
    pat = '.*?'.join(map(re.escape, search_string))
    pat = '(?=({0}))'.format(pat)   # lookahead regex to manage overlapping matches
    regex = re.compile(pat, re.IGNORECASE)

    idx = 0
    for item in collection:
        lst = accessor(item)
        if not isinstance(lst, list):
            lst = [lst]

        for s in lst:
            r = list(regex.finditer(s))
            if r:
                best = min(r, key=lambda x: len(x.group(1)))   # find shortest match
                suggestions.append((len(best.group(1)), best.start(), lst, item))
                idx += 1
                break

        if idx >= limit:
            break

    return (z[-1] for z in sorted(suggestions, key=lambda z: z[0]))
