import unittest

from src.htmlnode import LeafNode
from src.textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_text_type_eq(self):
        self.assertEqual(TextType.TEXT, TextType.TEXT)
        self.assertEqual(TextType.TEXT, TextType.TEXT.value)

    def test_text_type_neq(self):
        self.assertNotEqual(TextType.TEXT, TextType.BOLD)
        self.assertNotEqual(TextType.TEXT, TextType.BOLD.value)

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq_if_types_are_different(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_neq_if_text_is_different(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_neq_if_url_is_different(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.LINK, "https://www.google.com")
        self.assertNotEqual(node, node2)

    def test_neq_if_is_not_a_text_node(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.boot.dev")
        self.assertNotEqual(node, True)

    def test_text_node_to_html_node_text(self):
        node = text_node_to_html_node(TextNode("This is a text node", TextType.TEXT))
        self.assertTrue(isinstance(node, LeafNode))
        self.assertEqual(node.to_html(), "This is a text node")

    def test_text_node_to_html_node_bold(self):
        node = text_node_to_html_node(TextNode("This is a bold node", TextType.BOLD))
        self.assertTrue(isinstance(node, LeafNode))
        self.assertEqual(node.to_html(), "<b>This is a bold node</b>")

    def test_text_node_to_html_node_italic(self):
        node = text_node_to_html_node(TextNode("This is a italic node", TextType.ITALIC))
        self.assertTrue(isinstance(node, LeafNode))
        self.assertEqual(node.to_html(), "<i>This is a italic node</i>")

    def test_text_node_to_html_node_code(self):
        node = text_node_to_html_node(TextNode("This is a code node", TextType.CODE))
        self.assertTrue(isinstance(node, LeafNode))
        self.assertEqual(node.to_html(), "<code>This is a code node</code>")

    def test_text_node_to_html_node_link(self):
        node = text_node_to_html_node(TextNode("This is a link node", TextType.LINK, "https://domain.tld/"))
        self.assertTrue(isinstance(node, LeafNode))
        self.assertEqual(node.to_html(), '<a href="https://domain.tld/">This is a link node</a>')

    def test_text_node_to_html_node_img(self):
        node = text_node_to_html_node(TextNode("This is a image node", TextType.IMAGE, "https://domain.tld/image.png"))
        self.assertTrue(isinstance(node, LeafNode))
        self.assertEqual(node.to_html(), '<img src="https://domain.tld/image.png" alt="This is a image node"></img>')

    def test_text_node_to_html_node_invalid_type(self):
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            text_node_to_html_node(TextNode(text="This is a invalid node", text_type='invalid'))


if __name__ == "__main__":
    unittest.main()