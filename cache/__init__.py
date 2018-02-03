from abc import ABCMeta,abstractmethod


class CacheInterface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def store(self, key, contents):
        """
        Stores the contents into key
        """

    @abstractmethod
    def exists(self, key):
        """
        Returns True if contents are available
        """

    @abstractmethod
    def get(self, key):
        """
        Returns the contents for the key
        """
