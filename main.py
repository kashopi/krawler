from cache.filesystem import FileCache
from crawler import Crawler
import logging


logging.basicConfig(level=logging.INFO)
page = Crawler(FileCache()).get_page("https://google.es")
print(len(page))
