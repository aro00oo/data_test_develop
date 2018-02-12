from lxml import etree

from unittest import TestCase

from ..primary_elements import Listing
from ..xml_document_element import XmlDocumentElement


class TestElement(TestCase):
    """Test cases for the element property"""

    def test_with_invalid_input(self):
        """An invalid document input should blow up"""
        TEST_INVALID_DOCUMENT = 'TEST'
        with self.assertRaises(TypeError): #blow up here due to xml feed
            xmlDocElement = XmlDocumentElement(TEST_INVALID_DOCUMENT)
            with self.assertRaises(etree.XMLSyntaxError): #blow up here because the feed cant be parsed
                return xmlDocElement.element

    def test_with_valid_input(self):
        """A valid document should return an lxml element"""
        TEST_VALID_DOCUMENT = "<test></test>"
        xmlDocElement = XmlDocumentElement(TEST_VALID_DOCUMENT)
        self.assertIsInstance(xmlDocElement.element, etree._Element)


class TestGetPrimaryElements(TestCase):
    """Test cases for the get_primary_elements method"""
    CURRENTLY_IMPLEMENTED_ELEMENT_NAME = 'Listing'

    def test_with_non_implemented_element(self):
        """A non implemented element name should explode"""
        TEST_NON_IMPLEMENTED_ELEMENT = 'TEST'
        TEST_DOCUMENT = "<test></test>"
        xmlDocElement = XmlDocumentElement(TEST_DOCUMENT)
        with self.assertRaises(NotImplementedError):
            xmlDocElement.get_primary_elements(TEST_NON_IMPLEMENTED_ELEMENT)

    def test_with_empty_document(self):
        """An empty document should return an empty list"""
        TEST_EMPTY_DOCUMENT = "<test></test>"
        xmlDocElement = XmlDocumentElement(TEST_EMPTY_DOCUMENT)
        emptyResults = xmlDocElement.get_primary_elements(self.CURRENTLY_IMPLEMENTED_ELEMENT_NAME)
        self.assertEqual(emptyResults, [])

    def test_with_valid_document(self):
        """"A valid document should return a list of the implemented elements"""
        TEST_DOCUMENT = "<Listings><Listing><DateListed>2016-01-01 00:00:00</DateListed></Listing><Listing><DateListed>2017-01-01 00:00:00</DateListed></Listing></Listings>"
        xmlDocElement = XmlDocumentElement(TEST_DOCUMENT)
        results = xmlDocElement.get_primary_elements(self.CURRENTLY_IMPLEMENTED_ELEMENT_NAME)
        for result in results:
            self.assertIsInstance(result, Listing)