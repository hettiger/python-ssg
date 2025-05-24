import unittest

from src.base_path import base_path
from src.extract_title import extract_title


class MyTestCase(unittest.TestCase):
    def test_it_returns_the_title(self):
        expected_title = "Tolkien Fan Club"
        with open(base_path("content/index.md")) as file:
            markdown = file.read()

        actual_title = extract_title(markdown)

        self.assertEqual(expected_title, actual_title)

    def test_it_throws_an_error_if_no_title_is_found(self):
        markdown = "## h1 is mandatory"

        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_it_does_not_require_whitespace(self):
        expected_title = "H1 does not require whitespace"
        markdown = "#H1 does not require whitespace"

        actual_title = extract_title(markdown)

        self.assertEqual(expected_title, actual_title)


if __name__ == '__main__':
    unittest.main()
