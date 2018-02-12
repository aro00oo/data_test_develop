from .elements.primary_elements import Listing

class PrimaryElementsProcessor:
    """Processes the primary elements in an XmlDocumentElement for parsing"""
    ELEMENT_TYPES_TO_METHODS = {
        Listing:  'process_listing_elements'
    }

    def process(self, elements, elementType):
        """Find the function to call to process for given primary elements"""
        processFunction = self.ELEMENT_TYPES_TO_METHODS.get(elementType)
        return getattr(self, processFunction)(elements) if processFunction else elements

    def process_listing_elements(self, elements):
        """Processes listing elements"""
        validElements = [element for element in elements if element.year_listed == 2016]
        validElements.sort()
        return validElements