from unittest import TestCase
from mock import patch
from cache.filesystem import FileCache


class TestFilesystemCache(TestCase):

    def setUp(self):
        self.filecache = FileCache()

    @patch("os.path.isfile")
    def test_key_exists_returns_true(self, mock_isfile):
        mock_isfile.return_value = True
        res = self.filecache.exists('blah')
        name = self.filecache._get_filename('blah')
        self.assertTrue(res)
        mock_isfile.assert_called_once_with(name)
