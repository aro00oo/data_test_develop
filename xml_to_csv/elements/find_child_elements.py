
def find_child_elements(element, childElementName):
    """Given an element, return its children with a matching name"""
    return element.xpath('.//{}'.format(childElementName))