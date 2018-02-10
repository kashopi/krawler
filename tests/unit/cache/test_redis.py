from unittest import TestCase
from mock import patch
from cache.redis import RedisCache


class TestRedisCache(TestCase):

    def setUp(self):
        with patch("cache.redis.redis") as mock_redis:
            self.redis = mock_redis
            self.rediscache = RedisCache()

    def test_key_exists_returns_true(self):
        self.rediscache.exists("blah")
        self.redis.StrictRedis.return_value.exists.\
            assert_called_once_with("blah")
