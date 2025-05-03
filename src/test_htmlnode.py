import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(tag="div", props={"class": "test-class"})
        attributes = node.props_to_html()
        self.assertEqual(attributes, ' class="test-class"')

    def test_props_to_html_with_None_props(self):
        node = HTMLNode(tag="div")
        attributes = node.props_to_html()
        self.assertEqual(attributes, "")

    def test_props_to_html_with_empty_props(self):
        node = HTMLNode(tag="div", props={})
        attributes = node.props_to_html()
        self.assertEqual(attributes, "")

    def test_props_to_html_with_multiple_props(self):
        node = HTMLNode(tag="div", props={"class": "test-class", "id": "test-id"})
        attributes = node.props_to_html()
        self.assertEqual(attributes, ' class="test-class" id="test-id"')