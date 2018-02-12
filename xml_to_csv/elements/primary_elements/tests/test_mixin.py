from lxml import etree
from unittest import TestCase

from ..mixin import PrimaryElementMixin


class TestFindChildElement(TestCase):
    """Test cases for finding a child element"""

    def test_no_child(self):
        """An element with no matching children should return None"""
        TEST_ELEMENT = etree.fromstring("<test></test>")
        TEST_CHILD = "TEST"

        element = PrimaryElementMixin(TEST_ELEMENT)
        noResultChild = element.find_child_element(TEST_CHILD)
        self.assertEqual(noResultChild, None)

    def test_one_child(self):
        """An element with matching child should return that child"""
        TEST_ELEMENT = etree.fromstring("<test><TEST></TEST></test>")
        TEST_CHILD = "TEST"

        element = PrimaryElementMixin(TEST_ELEMENT)
        foundChild = element.find_child_element(TEST_CHILD)
        self.assertEqual(foundChild.tag,TEST_CHILD)

    def test_multiple_children(self):
        """An element with multiple matching children should return the first match"""
        TEST_CHILD_TAG = 'TEST'
        TEST_CHILD1_VALUE = '1'
        TEST_CHILD1 = "<TEST>{}</TEST>".format(TEST_CHILD1_VALUE)
        TEST_CHILD2 = "<TEST>2</TEST>"
        TEST_ELEMENT = etree.fromstring("<test>{0}{1}</test>".format(TEST_CHILD1, TEST_CHILD2))

        element = PrimaryElementMixin(TEST_ELEMENT)
        foundChild = element.find_child_element(TEST_CHILD_TAG)
        self.assertEqual(foundChild.text, TEST_CHILD1_VALUE)


class TestGetElementValue(TestCase):
    """Test cases for get_element_value function"""

    def test_no_element(self):
        """a none passed in should return an empty string"""
        TEST_NONE_ELEMENT = None
        noneElemValue = PrimaryElementMixin.get_element_value(TEST_NONE_ELEMENT)
        self.assertEqual(noneElemValue, '')

    def test_non_valid_element(self):
        """A not valid element passed in should blow up"""
        class NonValidElement:
            """A non valid element"""

        TEST_NON_VALID_ELEMENT = NonValidElement()
        with self.assertRaises(AttributeError):
            PrimaryElementMixin.get_element_value(TEST_NON_VALID_ELEMENT)

    def test_valid_element(self):
        """A valid element should return its text"""
        TEST_ELEMENT_VALUE = "Test"
        TEST_ELEMENT = etree.fromstring("<test>{}</test>".format(TEST_ELEMENT_VALUE))

        value = PrimaryElementMixin.get_element_value(TEST_ELEMENT)
        self.assertEqual(value, TEST_ELEMENT_VALUE)

class TestCreateValueForSubElements(TestCase):
    """Test Cases for the create_value_for_sub_elements function"""

    def test_no_element(self):
        """None should return empty string"""
        TEST_NONE_ELEMENT = None
        TEST_SUB_ELEMENT = 'TEST'
        value = PrimaryElementMixin.create_value_for_sub_elements(TEST_NONE_ELEMENT, TEST_SUB_ELEMENT)
        self.assertEqual(value, '')

    def test_sub_elements_not_found(self):
        """No sub elements should return an empty string"""
        TEST_ELEMENT = etree.fromstring("<test></test>")
        TEST_SUB_ELEMENT = "TEST"
        value = PrimaryElementMixin.create_value_for_sub_elements(TEST_ELEMENT, TEST_SUB_ELEMENT)
        self.assertEqual(value, '')

    def test_sub_elements_found(self):
        """Found sub elements should return a value"""
        EXPECTED_VALUE = "hello, world"
        TEST_ELEMENT = etree.fromstring("<test><TEST>hello</TEST><TEST>world</TEST></test>")
        TEST_SUB_ELEMENT = "TEST"
        value = PrimaryElementMixin.create_value_for_sub_elements(TEST_ELEMENT, TEST_SUB_ELEMENT)
        self.assertEqual(value, EXPECTED_VALUE)