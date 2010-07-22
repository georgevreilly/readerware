#!/usr/bin/env python

import csv
import re

re_conjunction = re.compile(r"[&:;]|\Wand\W", re.IGNORECASE)

def split_first_last_name(author_entry):
    names = [name.strip() for name in author_entry.split(",")]
    if len(names) == 1:
        names = [name.strip() for name in author_entry.split()]
        names = [names[-1], ' '.join(names[:-1])]
    return names

def split_multiple_authors(authors_entry):
    return [au.strip() for au in re_conjunction.split(authors_entry)]

def parse_csv(csv_filename):
    bookReader = csv.DictReader(open(csv_filename))
    items = [x for x in bookReader]
    # TODO: handle &doublequote;
    print len(items), bookReader.fieldnames
    
if __name__ == '__main__':
    from optparse import OptionParser
    import doctest
    import unittest

    class TestParsing(unittest.TestCase):
        def test_split_first_last_name(self):
            self.assertEqual(['Joyce', 'James'], split_first_last_name('Joyce, James'))
            self.assertEqual(["Moulitsas Zuniga", "Markos"], split_first_last_name("Moulitsas Zuniga, Markos"))
            self.assertEqual(["di Montezemolo", "Catherine"], split_first_last_name("di Montezemolo, Catherine"))
            self.assertEqual(["Rossi", "Jean Baptiste"], split_first_last_name("Rossi, Jean Baptiste"))
            self.assertEqual(["van Dam", "Andries"], split_first_last_name("van Dam, Andries"))
            self.assertEqual(["Aho", "Alfred V."], split_first_last_name("Aho, Alfred V."))
            self.assertEqual(["Elrod", "P. N."], split_first_last_name("P. N. Elrod"))
            self.assertEqual(["Woodham-Smith", "Cecil"], split_first_last_name("Cecil Woodham-Smith"))

        def test_split_multiple_authors(self):
            self.assertEqual(
                ["Armstrong, Jerome", "Moulitsas Zuniga, Markos"],
                split_multiple_authors("Armstrong, Jerome & Moulitsas Zuniga, Markos"))
            self.assertEqual(
                ["Flint, Eric", "Weber, David"],
                split_multiple_authors("Flint, Eric AND Weber, David"))
            self.assertEqual(
                ["Bodi, Jack", "Merrill, Meg", "di Montezemolo, Catherine"],
                split_multiple_authors("Bodi, Jack and Merrill, Meg and di Montezemolo, Catherine"))
            self.assertEqual(
                ["Pitxot, Antoni", "Aguer, Montse", "Puig, Jordi"],
                split_multiple_authors("Pitxot, Antoni & Aguer, Montse & Puig, Jordi"))
            self.assertEqual(
                ["Rossi, Jean Baptiste", "Sebastien Japrisot"],
                split_multiple_authors("Rossi, Jean Baptiste; Sebastien Japrisot"))
            self.assertEqual(
                ["Aho, Alfred V.", "Sethi, Ravi", "Ullman, Jeffrey D."],
                split_multiple_authors("Aho, Alfred V.; Sethi, Ravi; Ullman, Jeffrey D."))
            self.assertEqual(
                ["Duberman, Martin", "Vicinus, Martha", "Chauncey, George Jr. (editor)"],
                split_multiple_authors("Duberman, Martin; Vicinus, Martha & Chauncey, George Jr. (editor)"))
            self.assertEqual(
                ["Evjen, Bill", "Hanselman, Scott", "Muhammad, Farhan", "et al"],
                split_multiple_authors("Evjen, Bill; Hanselman, Scott; Muhammad, Farhan; et al"))
            self.assertEqual(
                ["Foley, James D.", "van Dam, Andries", "Feiner, Steven K.", "Hughes, John F."],
                split_multiple_authors("Foley, James D.: van Dam, Andries; Feiner, Steven K.; Hughes, John F."))
# "Hamilton, Laurell K. and MaryJanice Davidson, Eileen Wilks, Rebecca York"
# "Roghaar, Linda (Editor) and Wolf, Nancy"
# "Gies, Joseph and Francis"

    parser = OptionParser()
    parser.add_option("-t", "--test", action="store_true", dest="test",
                      default=False, help="run unit tests")
    parser.add_option("-f", "--file", dest="filename",
                      default="data/books2.csv", help="read CSV data from FILE", metavar="FILE")

    (options, args) = parser.parse_args()

    if options.test:
        test = unittest.defaultTestLoader.loadTestsFromModule( __import__('__main__') )
        unittest.TextTestRunner().run(test)
    else:
        parse_csv(options.filename)
