import unittest

from src.html_node import LeafNode
from src.node_utils import text_node_to_html_node, split_nodes_delimiter
from src.text_node import TextNode, TextType


class NodeUtilsTest(unittest.TestCase):
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

    def test_split_nodes_delimiter_bold(self):
        old_nodes = [TextNode("This is a **text** node", TextType.TEXT)]
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" node", TextType.TEXT),
        ]

        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

        self.assertEqual(expected, new_nodes)

    def test_split_nodes_delimiter_code(self):
        old_nodes = [TextNode("This is text with a `code block` word", TextType.TEXT)]
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)

        self.assertEqual(expected, new_nodes)

    def test_split_nodes_delimiter_only_italic(self):
        old_nodes = [TextNode("_This is italic text_", TextType.TEXT)]
        expected = [TextNode("This is italic text", TextType.ITALIC)]

        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)

        self.assertEqual(expected, new_nodes)

    def test_split_nodes_delimiter_multiple_matches(self):
        old_nodes = [TextNode("This is _italic_ text with _multiple_ matches", TextType.TEXT)]
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text with ", TextType.TEXT),
            TextNode("multiple", TextType.ITALIC),
            TextNode(" matches", TextType.TEXT),
        ]

        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)

        self.assertEqual(expected, new_nodes)

    def test_split_nodes_delimiter_no_matches(self):
        old_nodes = [TextNode("This is text with no delimiter matches", TextType.TEXT)]
        expected = [TextNode("This is text with no delimiter matches", TextType.TEXT)]

        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)

        self.assertEqual(expected, new_nodes)

    def test_split_nodes_delimiter_already_split(self):
        old_nodes = [TextNode("This is text is already split", TextType.CODE)]
        expected = [TextNode("This is text is already split", TextType.CODE)]

        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)

        self.assertEqual(expected, new_nodes)

    def test_split_nodes_delimiter_unclosed(self):
        old_nodes = [TextNode("This is _text is invalid markdown", TextType.CODE)]

        with self.assertRaises(ValueError):
            split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)

    def test_split_nodes_delimiter_empty_match(self):
        old_nodes = [TextNode("This is __ text", TextType.TEXT)]
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode(" text", TextType.TEXT),
        ]

        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)

        self.assertEqual(expected, new_nodes)


if __name__ == '__main__':
    unittest.main()
