#!/usr/bin/env python

import csv
import re

# TODO: check UTF-8 encoding

def normalize_name(last_name, first_name):
    # TODO: handle initials (esp. with period). Treat "L.Frank" as "L. Frank"; "DD" as "D.D."
    return (last_name, first_name)

re_et_al = re.compile(r"\s*[&;(]?\s*et al[.)]?\s*$", re.IGNORECASE)

def normalize_authors(authors_entry):
    """Strip a trailing 'et al'"""
    # TODO: strip (Foreword), (Translator), (Reader), (Director), (Preface), (trans.) (Photographer), (Text), (Illustrator)
    return re_et_al.sub("", authors_entry)

def split_first_last_name(author_entry):
    """Split `author_entry` into (last_name, first_name)."""
    # TODO: handle one-word names
    if ',' in author_entry:
        names = [name.strip() for name in author_entry.split(",")]
    else:
        names = [name.strip() for name in author_entry.split()]
        names = [names[-1], ' '.join(names[:-1])]
    return names

def split_authors2(authors):
    if authors.count(',') <= 1:
        return [authors.strip()]
    else:
        # Handle something like "Flintstone, Fred, Rubble, Barney"
        result, token = [], None
        for name in authors.split(","):
            if token is None:
                token = name.strip()
            else:
                result.append(token + ", " + name.strip())
                token = None
        return result

re_conjunction = re.compile(r"[&:;]|\Wand\W", re.IGNORECASE)

def split_multiple_authors(authors_entry):
    """Split authors separated by '&', ';' or 'and'"""
    authors = []
    for au in re_conjunction.split(authors_entry):
        authors.extend(split_authors2(au))
    return authors

re_editor = re.compile(r"\s+\(ed(itor)?[.s]?\)", re.IGNORECASE)

def strip_editor(authors_entry):
    """Strip "(editor)" and the like."""
    is_editor = re_editor.search(authors_entry) is not None
    if is_editor:
        authors_entry = re_editor.sub("", authors_entry)
    return is_editor, authors_entry

re_doublequote = re.compile(r"\&doublequote;")

def fix_doublequote(s):
    """Readerware uses &doublequote; to indicate a nested double quote. (Sigh)"""
    return re_doublequote.sub('"', s)

# TODO: add Name class

class Authors(object):
    def __init__(self, authors_entry):
        self.is_editor, authors_entry = strip_editor(authors_entry)
        authors = split_multiple_authors(authors_entry)
        names = [split_first_last_name(author) for author in authors]
        self.names = [normalize_name(last_name, first_name) for last_name, first_name in names]

    def __str__(self):
        return ("; ".join(["{0}, {1}".format(last_name, first_name)
                           for last_name, first_name in self.names]) +
                (" (ed.)" if self.is_editor else ""))

def parse_csv(csv_filename):
    bookReader = csv.DictReader(open(csv_filename))
    items = []
    for x in bookReader:
        for f in bookReader.fieldnames:
            x[f] = fix_doublequote(x[f])
        authors = Authors(x['AUTHOR'])
        print(authors)
        items.append(x)
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
            self.assertEqual(
                ["Cody, Liza", "Lewin, Michael Z.", "Lovesey, Peter"],
                split_multiple_authors("Cody, Liza, Lewin, Michael Z. & Lovesey, Peter"))
# "Hamilton, Laurell K. and MaryJanice Davidson, Eileen Wilks, Rebecca York"
# "Roghaar, Linda (Editor) and Wolf, Nancy"
# "Gies, Joseph and Francis"

        def test_normalize_authors(self):
            self.assertEqual(
                "Evjen, Bill; Hanselman, Scott; Muhammad, Farhan",
                normalize_authors("Evjen, Bill; Hanselman, Scott; Muhammad, Farhan; et al"))
            self.assertEqual(
                "Bodi, Jack and Merrill, Meg and di Montezemolo, Catherine",
                normalize_authors("Bodi, Jack and Merrill, Meg and di Montezemolo, Catherine"))
            self.assertEqual(
                "Chin, Frank",
                normalize_authors("Chin, Frank et al"))
            self.assertEqual(
                "Doyle, Roddy",
                normalize_authors("Doyle, Roddy (et al)"))

        def test_strip_editor(self):
            self.assertEqual(
                (True, "Duberman, Martin; Vicinus, Martha & Chauncey, George Jr."),
                strip_editor("Duberman, Martin; Vicinus, Martha & Chauncey, George Jr. (editor)"))
            self.assertEqual(
                (False, "Reader's Digest Editors"),
                strip_editor("Reader's Digest Editors"))
            self.assertEqual(
                (True, "Duby, Georges & Aries, Philippe"),
                strip_editor("Duby, Georges & Aries, Philippe (editors)"))
            self.assertEqual(
                (True, "Farmer, Joyce"),
                strip_editor("Farmer, Joyce (ed.)"))
            self.assertEqual(
                (True, "UCB Wellness Letter"),
                strip_editor("UCB Wellness Letter (Eds)"))

        def test_fix_doublequote(self):
            self.assertEqual(
                "\"I!\" Said the Demon",
                fix_doublequote("&doublequote;I!&doublequote; Said the Demon"))


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
