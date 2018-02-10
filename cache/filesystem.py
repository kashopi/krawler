import os

from cache import CacheInterface


class FileCache(CacheInterface):
    def store(self, key, contents):
        filename = self._get_filename(key)
        with open(filename, "wb") as fp:
            fp.write(contents)

    def exists(self, key):
        return os.path.isfile(self._get_filename(key))

    def get(self, key):
        return open(self._get_filename(key), "rb").read()

    def _get_filename(self, key):
        return ".cache/{}".format(key)
