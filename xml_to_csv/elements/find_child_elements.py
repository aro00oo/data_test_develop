
def find_child_elements(node, childElementName):
    """Given an element, return its children with a matching name"""
    return node.xpath('.//{}'.format(childElementName))