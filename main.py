import logging

from cache.filesystem import FileCache
from crawler import Crawler


logging.basicConfig(level=logging.INFO)
crawler = Crawler(FileCache())
page = crawler.get_page("https://google.es")
links = crawler.get_links(page)
print(links)
