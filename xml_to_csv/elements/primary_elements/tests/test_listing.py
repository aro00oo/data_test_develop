from lxml import etree
from unittest import TestCase

from ..listing import Listing


class TestListingProperties(TestCase):
    """Test cases for the Listing properties"""

    #only testing mls id as almost all other properties do the same thing (see as_csv for clarification)
    #again, could be more explicit but /shrug
    def test_no_mls_id(self):
        """An element with no mls id should return None"""
        TEST_ELEMENT = etree.fromstring("<test></test>")
        TEST_LISTING_ELEMENT = Listing(TEST_ELEMENT)
        self.assertIsNone(TEST_LISTING_ELEMENT.mls_id)

    def test_found_mls_id(self):
        """An element with an mls id should return it"""
        TEST_MLS_ID = 'TEST'
        TEST_ELEMENT = etree.fromstring("<test><MlsId>{}</MlsId></test>".format(TEST_MLS_ID))
        TEST_LISTING_ELEMENT = Listing(TEST_ELEMENT)
        self.assertEqual(TEST_LISTING_ELEMENT.mls_id.text, TEST_MLS_ID)


class TestSortListing(TestCase):
    """Test cases for sorting a Listing which also tests date_listed_as_datetime"""

    def test_with_no_date_listed(self):
        """With no dates, sorting should blow up with attribute errors all over the place"""
        TEST_ELEMENTS = [etree.fromstring("<test></test>") for i in range(3)]
        TEST_LISTING_ELEMENTS = [Listing(element) for element in TEST_ELEMENTS]
        with self.assertRaises(AttributeError):
            TEST_LISTING_ELEMENTS.sort()

    def test_with_date_listed(self):
        """With dates, sorting should return in ascending order"""
        TEST_LISTING_ELEMENT_FIRST = Listing(etree.fromstring("<test><DateListed>2016-01-01 00:00:00</DateListed></test>"))
        TEST_LISTING_ELEMENT_MIDDLE = Listing(etree.fromstring("<test><DateListed>2017-01-01 00:00:00</DateListed></test>"))
        TEST_LISTING_ELEMENT_LAST = Listing(etree.fromstring("<test><DateListed>2018-01-01 00:00:00</DateListed></test>"))
        TEST_LISTING_ELEMENTS = [TEST_LISTING_ELEMENT_MIDDLE, TEST_LISTING_ELEMENT_LAST, TEST_LISTING_ELEMENT_FIRST]
        TEST_LISTING_ELEMENTS.sort()
        self.assertEqual(TEST_LISTING_ELEMENTS[0], TEST_LISTING_ELEMENT_FIRST)
        self.assertEqual(TEST_LISTING_ELEMENTS[-1], TEST_LISTING_ELEMENT_LAST)

class TestAsCsv(TestCase):
    """Test cases for the as_csv method"""
    CURRENT_NUMBER_OF_COLUMNS_RETURNED = 10

    #Only testing using the three distinct types of properties of Listing (single val, multiple val, and description)
    def test_with_non_implemented_element(self):
        """As csv should still return a list with empty values with an empty listing"""
        TEST_LISTING_ELEMENT = Listing(etree.fromstring("<test><TESTTAG></TESTTAG></test>"))
        CURRENT_NUMBER_OF_COLUMNS = 10

        asCsvResult = TEST_LISTING_ELEMENT.as_csv()
        self.assertEqual(len(asCsvResult), CURRENT_NUMBER_OF_COLUMNS)
        for columnVal in asCsvResult:
            self.assertEqual(columnVal, '')

    def test_with_single_val_property(self):
        """As csv should include a property that returns a single value, e.g. MlsId"""
        TEST_MLD_ID_VALUE = "TEST"
        TEST_LISTING_ELEMENT = Listing(etree.fromstring("<test><MlsId>{}</MlsId></test>".format(TEST_MLD_ID_VALUE)))

        asCsvResult = TEST_LISTING_ELEMENT.as_csv()
        self.assertEqual(len(asCsvResult), self.CURRENT_NUMBER_OF_COLUMNS_RETURNED)
        self.assertIn(TEST_MLD_ID_VALUE, asCsvResult)

    def test_with_multiple_val_property(self):
        """As csv should include multiple val properties, e.g. Appliances"""
        TEST_SUB_ELEMENT = 'TEST1'
        TEST_SUB_ELEMENT2 = 'TEST2'
        TEST_EXPECTED_VALUE = "{0}, {1}".format(TEST_SUB_ELEMENT, TEST_SUB_ELEMENT2)
        TEST_LISTING_ELEMENT = Listing(etree.fromstring("<test><Appliances><Appliance>{0}"
                                                        "</Appliance><Appliance>{1}</Appliance></Appliances></test>".format(TEST_SUB_ELEMENT, TEST_SUB_ELEMENT2)))

        asCsvResult = TEST_LISTING_ELEMENT.as_csv()
        self.assertEqual(len(asCsvResult), self.CURRENT_NUMBER_OF_COLUMNS_RETURNED)
        self.assertIn(TEST_EXPECTED_VALUE, asCsvResult)

    def test_with_description(self):
        """As csv should include only the first 200 char of a description element"""
        TEST_DESCRIPTION_VALUE = " ".join([str(i) for i in range(400)])
        TEST_EXPECTED_RESULT = TEST_DESCRIPTION_VALUE[:200]
        TEST_LISTING_ELEMENT = Listing(etree.fromstring("<test><Description>{}</Description></test>".format(TEST_DESCRIPTION_VALUE)))

        asCsvResult = TEST_LISTING_ELEMENT.as_csv()
        self.assertEqual(len(asCsvResult), self.CURRENT_NUMBER_OF_COLUMNS_RETURNED)
        self.assertNotIn(TEST_DESCRIPTION_VALUE, asCsvResult)
        self.assertIn(TEST_EXPECTED_RESULT, asCsvResult)

    def test_with_all_property_types(self):
        """ALl three types of properties should be included"""

        TEST_MLD_ID_VALUE = "TEST"
        TEST_SUB_ELEMENT = 'TEST1'
        TEST_SUB_ELEMENT2 = 'TEST2'
        TEST_EXPECTED_SUB_ELEMENTS_VALUE = "{0}, {1}".format(TEST_SUB_ELEMENT, TEST_SUB_ELEMENT2)
        TEST_DESCRIPTION_VALUE = " ".join([str(i) for i in range(400)])
        TEST_EXPECTED_DESCRIPTION = TEST_DESCRIPTION_VALUE[:200]

        TEST_LISTING_ELEMENT = Listing(etree.fromstring(
            """<test>
                    <MlsId>{0}</MlsId>
                    <Appliances>
                        <Appliance>{1}</Appliance>
                        <Appliance>{2}</Appliance>
                    </Appliances>
                    <Description>{3}</Description>
                </test>"""
            .format(TEST_MLD_ID_VALUE, TEST_SUB_ELEMENT, TEST_SUB_ELEMENT2, TEST_DESCRIPTION_VALUE)))

        asCsvResult = TEST_LISTING_ELEMENT.as_csv()
        self.assertEqual(len(asCsvResult), self.CURRENT_NUMBER_OF_COLUMNS_RETURNED)
        self.assertIn(TEST_MLD_ID_VALUE, asCsvResult)
        self.assertIn(TEST_EXPECTED_SUB_ELEMENTS_VALUE, asCsvResult)
        self.assertIn(TEST_EXPECTED_DESCRIPTION, asCsvResult)
