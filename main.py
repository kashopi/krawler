import logging
import redis
from cache.redis import RedisCache
from crawler import Crawler


logging.basicConfig(level=logging.INFO)

redis_connection = redis.StrictRedis(host='localhost', port=6379, db=0)
crawler = Crawler(RedisCache(redis_connection), redis_connection)
crawler.start()
