import unittest

from htmlnode import HTMLNode
from src.htmlnode import LeafNode, ParentNode


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
        node = HTMLNode(tag="div", props={"id": "test-id", "class": "test-class"})
        attributes = node.props_to_html()
        self.assertEqual(attributes, ' id="test-id" class="test-class"')

    def test_leaf_node_with_None_value(self):
        with self.assertRaises(ValueError):
            LeafNode(tag="p", value=None)

    def test_leaf_node_to_html(self):
        node = LeafNode(tag="p", value="Hello World!")
        html = node.to_html()
        self.assertEqual(html, "<p>Hello World!</p>")

    def test_leaf_node_to_html_with_props(self):
        node = LeafNode(tag="p", value="Hello World!", props={"id": "test-id", "class": "test-class"})
        html = node.to_html()
        self.assertEqual(html, '<p id="test-id" class="test-class">Hello World!</p>')

    def test_leaf_node_to_html_without_tag(self):
        node = LeafNode(tag=None, value="Hello World!")
        html = node.to_html()
        self.assertEqual(html, "Hello World!")

    def test_parent_node_without_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(tag=None, children=[])

    def test_parent_node_without_children(self):
        with self.assertRaises(ValueError):
            ParentNode(tag="div", children=None)

    def test_parent_node_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        html = node.to_html()
        self.assertEqual(html,"<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_parent_node_to_html_with_children(self):
        node = ParentNode("div", [
            LeafNode("span", "child")
        ])
        self.assertEqual(node.to_html(), "<div><span>child</span></div>")

    def test_parent_node_to_html_with_grandchildren(self):
        node = ParentNode("div", [
            ParentNode("span", [
                LeafNode("b", "grandchild")
            ])
        ])
        self.assertEqual(
            node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_node_to_html_with_empty_children(self):
        node = ParentNode(tag="div", children=[])
        html = node.to_html()
        self.assertEqual(html, "<div></div>")

    def test_parent_node_to_html_with_parent_as_child(self):
        node = ParentNode("div", [
            ParentNode("div", [])
        ])
        html = node.to_html()
        self.assertEqual(html, "<div><div></div></div>")
