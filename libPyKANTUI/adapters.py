# -*- coding: utf-8 -*-

import itertools

from libPyKAN import ckanRepo
from libPyKAN.pykancfg import PyKANSettings
from libPyKAN.installed import Installed

from libPyKANTUI import util

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
            mod_list_it = util.fuzzy.find(fuzzyfindtext, mod_list_it, lambda mod: [mod.identifier, mod.name])

        # Limit
        mod_list_it = itertools.islice(mod_list_it, limit)

        # Make list and return
        return list(mod_list_it)
