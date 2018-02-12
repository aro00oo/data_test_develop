import os
import requests

from urlparse import urlparse


class XmlFeed:
    """Represents some type of xml feed into a normalized feed """
    def __init__(self, input):
        self.input = input

    def __enter__(self, *args, **kwargs):
        """Initialize the input as a feed"""
        if self.is_url:
            self.feed = requests.get(self.input).content
        elif self.is_file:
            self.feed = open(self.input, 'rb')
        elif isinstance(self.input, str):
            self.feed = self.input
        else:
            raise TypeError("Please provide a parse-able input [file/url/text].")

        return self

    def __exit__(self, *args, **kwargs):
        """Close the feed if this is a file"""
        if self.is_file:
            self.feed.close()
        return self

    @property
    def is_url(self):
        """The input is a URL type"""
        parsedUrlResult = urlparse(self.input)
        return bool(parsedUrlResult.scheme and parsedUrlResult.netloc)

    @property
    def is_file(self):
        """The input is a file"""
        return os.path.isfile(self.input)
