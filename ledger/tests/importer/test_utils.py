import unittest

from ledger.importer.utils import find_comma_indexes, split_string


class TestFindCommaIndexes(unittest.TestCase):
    def test_no_commas(self):
        string = "This is a test string"
        self.assertEqual(find_comma_indexes(string), [])

    def test_with_commas(self):
        string = "Hello, world, this, is, a, string"
        self.assertEqual(find_comma_indexes(string), [5, 12, 18, 22, 25])

    def test_only_commas(self):
        string = ",,,,,,"
        self.assertEqual(find_comma_indexes(string), [0, 1, 2, 3, 4, 5])

    def test_empty_string(self):
        string = ""
        self.assertEqual(find_comma_indexes(string), [])


class TestSplitString(unittest.TestCase):
    def test_basic_split(self):
        string = "Hello, world, this, is, a, string"
        end_markers = [6, 13, 19, 23, 26]
        self.assertEqual(
            split_string(string, end_markers),
            ["Hello,", " world,", " this,", " is,", " a,", " string"],
        )

    def test_no_markers(self):
        string = "This is a test string"
        end_markers = []
        self.assertEqual(split_string(string, end_markers), [string])

    def test_empty_string(self):
        string = ""
        end_markers = []
        self.assertEqual(split_string(string, end_markers), [string])

    def test_single_marker(self):
        string = "This is a test string"
        end_markers = [4]
        self.assertEqual(
            split_string(string, end_markers), ["This", " is a test string"]
        )
