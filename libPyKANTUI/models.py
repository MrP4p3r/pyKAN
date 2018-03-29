# -*- coding: utf-8 -*-


class Mod:
    """Mod model."""

    def __init__(self, identifier, name, version, status):
        self.identifier = identifier
        self.name = name
        self.version = version
        self.status = status

    def __str__(self):
        return self.name

    @classmethod
    def from_dict(cls, dct):
        return cls(
            identifier=dct['identifier'],
            name=dct['name'],
            version=dct['version'],
            status=dct['status'],
        )

    def to_dict(self):
        return {
            'identifier': self.identifier,
            'name': self.name,
            'version': self.version,
            'status': self.status,
        }
