from unittest import TestCase

from mock.mock import Mock, patch

from crawler import Crawler, USER_AGENT


class CrawlerTest(TestCase):
    def setUp(self):
        self.cache = Mock()

    def test_is_valid_link(self):
        links_config = ((False, ['blah']),
                        (True, ['href', 'blahbluh']))
        crawler = Crawler(self.cache)
        mock_link = Mock()
        for value, attrs in links_config:
            mock_link.attrs = attrs
            self.assertEqual(value, crawler._is_valid_link(mock_link))

    def test_init_sets_user_agent(self):
        crawler = Crawler(self.cache)
        self.assertEqual(USER_AGENT, crawler._headers['User-agent'])

    @patch("crawler.Crawler._get_key")
    def test_get_url_contents_checks_cache(self, mock_get_key):
        mock_get_key.return_value = "abc"
        crawler = Crawler(self.cache)
        with patch('crawler.requests') as mock_requests:
            crawler._get_url_contents("myurl")
            self.cache.exists.assert_called_once_with('abc')

    @patch("crawler.Crawler._get_key")
    def test_get_url_does_not_request_when_cached(self, mock_get_key):
        mock_get_key.return_value = "abc"
        crawler = Crawler(self.cache)
        self.cache.exists.return_value = True
        with patch('crawler.requests') as mock_requests:
            crawler._get_url_contents("myurl")
            self.assertFalse(mock_requests.get.called)

    @patch("crawler.Crawler._get_key")
    def test_get_url_requests_when_not_cached(self, mock_get_key):
        mock_get_key.return_value = "abc"
        crawler = Crawler(self.cache)
        self.cache.exists.return_value = False
        with patch('crawler.requests') as mock_requests:
            crawler._get_url_contents("myurl")
            mock_requests.get.assert_called_once_with(
                "myurl", headers=crawler._headers)
