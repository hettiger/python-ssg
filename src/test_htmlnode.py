import unittest

from htmlnode import HTMLNode
from src.htmlnode import LeafNode


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

    def test_leaf_node_to_html(self):
        node = LeafNode(tag="p", value="Hello World!")
        html = node.to_html()
        self.assertEqual(html, "<p>Hello World!</p>")

    def test_leaf_node_to_html_without_tag(self):
        node = LeafNode(tag=None, value="Hello World!")
        html = node.to_html()
        self.assertEqual(html, "Hello World!")

    def test_leaf_node_to_html_with_None_value(self):
        node = LeafNode(tag="p", value=None)
        with self.assertRaises(ValueError):
            node.to_html()

