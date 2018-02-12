import csv

from .elements import XmlDocumentElement

class XmlToCsv:
    """Parses an XmlDocument for its primary Elements"""
    def __init__(self, xmlDocument):
        self.document = XmlDocumentElement(xmlDocument)

    def create_csv_file(self, primaryElemName, outputFileDestination):
        """Turn the XML document into a csv at a given destination """
        with open(outputFileDestination, 'wb') as outputCsv:
            csvWriter = csv.writer(outputCsv)
            for primaryElem in self.document.get_primary_elements(primaryElemName):
                csvWriter.writerow(primaryElem.as_csv())
