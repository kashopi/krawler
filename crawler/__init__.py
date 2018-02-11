from hashlib import md5
import logging

from bs4 import BeautifulSoup
import requests
from time import sleep


USER_AGENT = ("Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36")


class Crawler(object):
    def __init__(self, cache_manager, redis_connection):
        logging.info("Starting Crawler...")
        self._cache_manager = cache_manager
        self._redis_connection = redis_connection
        self._headers = {}
        self._set_user_agent()

    def start(self):
        logging.info("Starting subscriber...")
        self._create_pubsub()
        self._redis_connection.publish('crawler-pubsub', "https://google.es")
        while True:
            message = self._pubsub.get_message()
            self._process_message(message)
            sleep(1)

    def _process_message(self, message):
        if message['type']=='message':
            logging.info("Received URL: %s", message)
            page = self.get_page(message['data'].decode('ascii'))
            links = self.get_links(page)
            self._process_links(links)
        elif message:
            logging.info("Received: %s", message)

    def _process_links(self, links):
        for link in links:
            self._redis_connection.publish('crawler-pubsub', link)

    def _create_pubsub(self):
        self._pubsub = self._redis_connection.pubsub()
        self._pubsub.subscribe('crawler-pubsub')

    def get_page(self, url):
        logging.info("Get page %s...", url)
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

    def _get_key(self, data):
        return md5(data.encode('utf-8')).hexdigest()

    def _get_url_contents(self, url):
        key = self._get_key(url)
        if self._cache_manager.exists(key):
            logging.info("Contents found in cache")
            return self._cache_manager.get(key)

        response = requests.get(url, headers=self._headers)
        self._cache_manager.store(key,
                                  response.content)
        return response.content

    def _set_user_agent(self):
        self._headers['User-agent'] = USER_AGENT
