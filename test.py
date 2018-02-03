from abc import ABCMeta,abstractmethod
from hashlib import md5
import logging
import os
import requests


USER_AGENT = ("Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 "
             "(KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36")


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


class FileCache(CacheInterface):
    def store(self, key, contents):
        filename = self._get_filename(key)
        with open(filename, "wb") as fp:
            fp.write(contents)

    def exists(self, key):
        return(os.path.isfile(self._get_filename(key)))

    def get(self, key):
        return(open(self._get_filename(key),
                    "rb").read())

    def _get_filename(self, key):
        return "cache/{}".format(key)


class Crawler(object):
    def __init__(self, cache_manager):
        logging.info("Starting Crawler...")
        self._cache_manager = cache_manager
        self._headers = {}
        self._set_user_agent()

    def get_page(self, url):
        return(self._get_url_contents(url))

    def _get_url_contents(self, url):
        key = md5(url.encode('utf-8')).hexdigest()
        if self._cache_manager.exists(key):
            logging.info("Contents found in cache")
            return(self._cache_manager.get(key))

        response = requests.get(url, headers=self._headers)
        self._cache_manager.store(key,
                                  response.content)
        return(response.content)

    def _set_user_agent(self):
        self._headers['User-agent'] = USER_AGENT


logging.basicConfig(level=logging.INFO)
page = Crawler(FileCache()).get_page("https://google.es")
print(len(page))

