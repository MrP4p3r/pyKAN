# -*- coding: utf-8 -*-

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

    def list_installed(self):
        return list(map(Mod.from_dict, self._installed.list_modules()))

    def list_all(self, limit=100):
        if limit:
            it = self._repo.list_modules()
            dct_list = [next(it) for _ in range(limit)]
        else:
            dct_list = list(self._repo.list_modules())
        return list(map(Mod.from_dict, dct_list))
