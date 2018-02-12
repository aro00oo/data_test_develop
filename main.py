

if __name__ == '__main__':
    import argparse

    from xml_to_csv import XmlToCsv

    parser = argparse.ArgumentParser(description="Write an XML input to a CSV file")

    parser.add_argument('-i', action='store', dest='input',
                        help='The input file/url/string')

    parser.add_argument('-o', action='store', dest='output',
                        help='The output file destination.')

    parser.add_argument('-n', action='store',
                        dest='name',
                        help='Primary element name, e.g. Listing')

    results = parser.parse_args()

    xmlToCsv = XmlToCsv(results.input)
    xmlToCsv.create_csv_file(results.name, results.output)