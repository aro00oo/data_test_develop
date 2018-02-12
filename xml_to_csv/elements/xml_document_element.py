import csv

from lxml import etree

from ..xml_feed import XmlFeed

from .find_child_elements import find_child_elements
from .primary_elements import Listing

#map primary element strings into their types, should probably be a different file
primaryElementMapper = {'Listing': Listing}


class XmlDocumentElement:
    """XML document represented as an element (lxml)"""
    def __init__(self, input):
        with XmlFeed(input) as xmlFeed:
            self.feed = xmlFeed.feed

    @property
    def element(self):
        """The Xml feed represented as an element (lxml)"""
        return etree.fromstring(self.feed)

    def get_primary_elements(self, primaryElemName):
        """The primary elements for this xml document (assumed a container of elements)"""
        if primaryElemName not in primaryElementMapper:
            raise NotImplementedError("This element is not yet implemented.")
        primaryElement = primaryElementMapper.get(primaryElemName)
        return [primaryElement(childElem) for childElem in find_child_elements(self.element, primaryElemName)]