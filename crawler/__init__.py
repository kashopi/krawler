from hashlib import md5
import logging

import requests
from bs4 import BeautifulSoup


USER_AGENT = ("Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36")


class Crawler(object):
    def __init__(self, cache_manager):
        logging.info("Starting Crawler...")
        self._cache_manager = cache_manager
        self._headers = {}
        self._set_user_agent()

    def get_page(self, url):
        return self._get_url_contents(url)

    def get_links(self, text):
        links_list = {}
        soup = BeautifulSoup(text, "html.parser")
        for link in soup.find_all('a'):
            if self._is_valid_link(link):
                name, href = self._process_link(link)
                logging.debug("Found link: %s", name)
                links_list[href] = name
        return links_list

    def _is_valid_link(self, link):
        return True if 'href' in link.attrs else False

    def _process_link(self, link):
        return link.text, link.attrs.get('href')

    def _get_url_contents(self, url):
        key = md5(url.encode('utf-8')).hexdigest()
        if self._cache_manager.exists(key):
            logging.info("Contents found in cache")
            return self._cache_manager.get(key)

        response = requests.get(url, headers=self._headers)
        self._cache_manager.store(key,
                                  response.content)
        return response.content

    def _set_user_agent(self):
        self._headers['User-agent'] = USER_AGENT
