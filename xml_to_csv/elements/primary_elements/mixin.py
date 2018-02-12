from ..find_child_elements import find_child_elements


class PrimaryElementMixin:
    """a mixin to provide common functionality for primary elements"""

    def __init__(self, listingElement):
        self.element = listingElement

    def find_child_element(self, childName):
        """Find a matching child element for this listing"""
        matchingElements =  find_child_elements(self.element, childName)
        return matchingElements[0] if matchingElements else None

    def get_element_value(self, elem):
        """Return the element's value"""
        return elem.text if elem is not None else ''

    def create_value_for_sub_elements(self, mainElem, subElemName):
        """Create a value for sub elements"""
        if mainElem is None:
            return ''

        subElements = mainElem.xpath('.//{}'.format(subElemName))
        if not subElements:
            value = ''
        else:
            value = ', '.join([subElement.text for subElement in subElements])
        return value