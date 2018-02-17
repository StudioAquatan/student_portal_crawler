import hashlib

from .shibboleth_login import ShibbolethClient


class PortalBrowser(object):
    """
    Singleton object to access KIT portal.
    """

    _instances = dict()

    def __new__(cls, username: str, password: str) -> ShibbolethClient:
        """Always return same instance against given username and password"""
        obj_hash = cls._calculate_hash(username, password)
        if obj_hash in cls._instances.keys():
            return cls._instances[obj_hash]
        cls._instances[obj_hash] = ShibbolethClient(username, password)
        return cls._instances[obj_hash]

    @staticmethod
    def _calculate_hash(username: str, password: str):
        """Calculate hash based on given username and password"""
        chars = (username + password).encode("utf-8")
        return hashlib.sha1(chars).hexdigest()
