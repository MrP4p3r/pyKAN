# -*- coding: utf-8 -*-

from libPyKAN import ckanRepo
from libPyKAN.pykancfg import PyKANSettings
from libPyKAN.installed import Installed


from .models import Mod


class PyKanComposite(object):

    def __init__(self):
        self._kspdir = None
        self._settings = PyKANSettings(self._kspdir)

        self._repo = ckanRepo.CkanRepo(self._settings)
        self._installed = Installed(self._settings, self._repo)
        self._settings.reload()

    def list_installed(self):
        return list(map(Mod.from_dict, self._installed.list_modules()))
