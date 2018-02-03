from hashlib import md5
import logging
import requests


USER_AGENT = ("Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 "
             "(KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36")


class Crawler(object):
    def __init__(self, cache_manager):
        logging.info("Starting Crawler...")
        self._cache_manager = cache_manager
        self._headers = {}
        self._set_user_agent()

    def get_page(self, url):
        return(self._get_url_contents(url))

    def get_links(self, text):
        pass

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
