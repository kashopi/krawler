import logging

from cache import CacheInterface


class RedisCache(CacheInterface):

    def __init__(self, connection):
        super(RedisCache, self).__init__()
        logging.info("Connecting Redis")
        self._redis = connection

    def store(self, key, contents):
        self._redis.set(key, contents)

    def exists(self, key):
        return self._redis.exists(key)

    def get(self, key):
        return self._redis.get(key)
