# Luke's Submission

### Script Requirements:
- Run $ pip install -r requirements.txt (http://lxml.de/installation.html for more info for lxml if unable to install)
- To run: $ python (assumed python2.7) main.py -i [input file/url/string] -o [outputfilepath] -n [primaryelementname]
    - For the exercise, the primary element name is "Listing"
    - e.g. python main.py -i http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml -o /output.csv -n Listing

### Unit Tests
- To run: $ python (assumed python2.7) -m unittest discover

### Other Thoughts

- The modular stipulation was the most difficult for me given the constraints of the output. Not sure how I was supposed to reconcile
the "required fields" stipulation with making it as modular as possible. I could have written it so it just spit out all
the nodes for a primary element to different rows, but the "required fields" stipulation made that not feasible. So, I just
went with having to implement a wrapper class for any future xml document to-be-parsed. Here, Listing is defined and it provides
the interface for being it written into a CSV row (along with a processor class to parse the data more if necessary).

- Couple assumptions I made include:
    - That all incoming xml documents are a container-behaving document (the test case is a Listings container of Listing elements)
    - That the first child element is the one we want, I saw several records with multiple StreetAddress, Description
    and other elements. If that was a wrong assumption, I could just join the values of the multiple records, but I just
    used that logic only for the ones that had the "all sub-nodes comma joined" stipulation.

- Missed unittest on the XmlToCsv and PrimaryElementsProcessor classes as I remembered the "please don't spend too much time"
request :D, unittests definitely took the most time.