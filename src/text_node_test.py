import unittest

from src.text_node import TextNode, TextType


class TextNodeTest(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()