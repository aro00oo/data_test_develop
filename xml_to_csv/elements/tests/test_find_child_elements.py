from lxml import etree
from unittest import TestCase

from ..find_child_elements import find_child_elements

class TestFindChildElements(TestCase):
    """Test cases for the find_child_elements function"""

    def test_invalid_param_type(self):
        """Should fail if a non lxml element type is passed in"""
        class InvalidElement:
            """An invalid element"""

        TEST_INVALID_ELEMENT = InvalidElement()
        TEST_CHILD_ELEM_NAME = 'TEST'
        with self.assertRaises(AttributeError):
            find_child_elements(TEST_INVALID_ELEMENT, TEST_CHILD_ELEM_NAME)

    def test_valid_params_empty_result(self):
        """Given a lxml element the function should run and return an empty list with no results"""
        TEST_ELEMENT = etree.fromstring("<test></test>")
        TEST_CHILD = "TESTCHILD"

        emptyResults = find_child_elements(TEST_ELEMENT, TEST_CHILD)
        self.assertEqual(emptyResults, [])

    def test_valid_params_found_result(self):
        """Given an lxml element and matching child, function should return the child inside a list"""
        TEST_ELEMENT = etree.fromstring("<test><TESTCHILD></TESTCHILD></test>")
        TEST_CHILD = "TESTCHILD"

        results = find_child_elements(TEST_ELEMENT, TEST_CHILD)
        self.assertEqual([result.tag for result in results], [TEST_CHILD])
