import logging
import redis

from cache import CacheInterface


class RedisCache(CacheInterface):

    def __init__(self):
        super(RedisCache, self).__init__()
        logging.info("Connecting Redis")
        self._redis = redis.StrictRedis(host='localhost', port=6379, db=0)

    def store(self, key, contents):
        self._redis.set(key, contents)

    def exists(self, key):
        return self._redis.exists(key)

    def get(self, key):
        return self._redis.get(key)
