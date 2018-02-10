import logging

from cache.redis import RedisCache
from crawler import Crawler


logging.basicConfig(level=logging.INFO)
crawler = Crawler(RedisCache())
# page = crawler.get_page("https://google.es")
page = crawler.get_page("https://www.simracingcoach.com/")
links = crawler.get_links(page)
logging.info("Found %d links", len(links.keys()))