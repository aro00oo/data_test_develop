from mock import patch, MagicMock, PropertyMock, Mock
from unittest import TestCase, main

from ..xml_feed import XmlFeed


class TestEnter(TestCase):
    """Various cases for the enter method"""

    @patch('xml_to_csv.xml_feed.requests')
    def test_enter_with_url(self, requestsPatch):
        """Ensure requests and response.content gets called"""
        TEST_URL = "http://test.com"
        getMethod = MagicMock()
        getMethodReturnValue = Mock()
        getMethod.return_value = getMethodReturnValue
        contentPropertyMock = PropertyMock()
        type(getMethodReturnValue).content = contentPropertyMock
        requestsPatch.get = getMethod
        with XmlFeed(TEST_URL) as feed:
            self.assertTrue(feed.is_url)
            self.assertFalse(feed.is_file)
            pass
        getMethod.assert_called_with(TEST_URL)
        contentPropertyMock.assert_called()

    @patch('xml_to_csv.xml_feed.open')
    @patch('xml_to_csv.xml_feed.os')
    def test_enter_with_file(self, osPatch, openPatch):
        """Ensure file is opened"""
        TEST_FILE = '/test/testfile.test'
        FILE_MODE = 'rb'
        with XmlFeed(TEST_FILE) as feed:
            self.assertTrue(feed.is_file)
            self.assertFalse(feed.is_url)

        openPatch.assert_called_with(TEST_FILE, FILE_MODE)

    def test_enter_with_string(self):
        TEST_INPUT_STR = "<body><h1>hello world</h1></body>"
        with XmlFeed(TEST_INPUT_STR) as feed:
            self.assertFalse(feed.is_file)
            self.assertFalse(feed.is_url)

    def test_enter_with_invalid_string(self):
        TEST_INPUT_STR = "TEST"
        with self.assertRaises(TypeError):
            with XmlFeed(TEST_INPUT_STR) as feed:
                self.assertFalse(feed.is_file)
                self.assertFalse(feed.is_url)

class TestExit(TestCase):
    """Case for the exit method"""

    #Only testing with file as that's the only interesting portion implemented
    #One might argue still make explicit tests for it given the enter method above, but /shrug

    @patch('xml_to_csv.xml_feed.open')
    @patch('xml_to_csv.xml_feed.os')
    def test_exit_with_file(self, osPatch, openPatch):
        """Ensure file is closed"""
        TEST_FILE = '/test/testfile.test'

        openMockReturnValue = Mock()
        closeMethodMock = MagicMock()
        openMockReturnValue.close = closeMethodMock
        openPatch.return_value = openMockReturnValue

        with XmlFeed(TEST_FILE) as feed:
            self.assertTrue(feed.is_file)
            self.assertFalse(feed.is_url)
        closeMethodMock.assert_called()
