from datetime import datetime

from ..find_child_elements import find_child_elements

from .mixin import PrimaryElementMixin


class Listing(PrimaryElementMixin):
    """Wraps a Listing lxml element"""

    def __lt__(self, other):
        """Implement the < operator for sorting"""
        return self.date_listed_as_datetime < other.date_listed_as_datetime

    @property
    def mls_id(self):
        """The element for the MLS id of this listing"""
        return self.find_child_element('MlsId')

    @property
    def mls_name(self):
        """The element for the MLS name of this listing"""
        return self.find_child_element('MlsName')

    @property
    def date_listed(self):
        """The element for date this listing was listed"""
        return self.find_child_element("DateListed")

    @property
    def street_address(self):
        """The element for address of this listing"""
        return self.find_child_element('StreetAddress')

    @property
    def price(self):
        """The element for the price of this listing"""
        return self.find_child_element('Price')

    @property
    def bedroom(self):
        """The element for the first bedroom of this listing"""
        return self.find_child_element('Bedrooms')

    @property
    def bathroom(self):
        """The element for the first bathroom of this listing"""
        return self.find_child_element('Bathrooms')

    @property
    def appliances(self):
        """The element for the appliances for this listing"""
        return self.find_child_element('Appliances')

    @property
    def rooms(self):
        """The element for the rooms for this listng"""
        return self.find_child_element('Rooms')

    @property
    def descriptions(self):
        """The element for the description for this listing """
        return self.find_child_element('Description')

    @property
    def date_listed_as_datetime(self):
        """The date listed property as a datetime object"""
        #assumes date listed always will exist
        dateListedVal = self.date_listed.text
        return datetime.strptime(dateListedVal, '%Y-%m-%d %H:%M:%S')

    @property
    def year_listed(self):
        """The year this listing was listed"""
        return self.date_listed_as_datetime.year

    def as_csv(self):
        """Represent a listing as a row for the csv"""
        singleValColumnElements = [self.mls_id, self.mls_name, self.date_listed, self.street_address, self.price, self.bedroom,
                          self.bathroom]
        listingColumnValues = []
        for element in singleValColumnElements:
            elementVal = self.get_element_value(element)
            listingColumnValues.append(elementVal)

        appliancesColumnVal = self.create_value_for_sub_elements(self.appliances, 'Appliance')
        listingColumnValues.append(appliancesColumnVal)

        roomsColumnVal = self.create_value_for_sub_elements(self.rooms, 'Room')
        listingColumnValues.append(roomsColumnVal)

        descriptionColumnVal = self.get_element_value(self.descriptions)
        listingColumnValues.append(descriptionColumnVal[:200])
        return listingColumnValues