from unittest import TestCase
from mock.mock import Mock
from cache.redis import RedisCache


class TestRedisCache(TestCase):

    def setUp(self):
        self.redis = Mock()
        self.rediscache = RedisCache(self.redis)

    def test_key_exists_returns_true(self):
        self.rediscache.exists("blah")
        self.redis.exists.assert_called_once_with("blah")
