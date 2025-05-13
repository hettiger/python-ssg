import unittest

from src.html_node import LeafNode
from src.utils import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, \
    split_nodes_image, split_nodes_link, pipeline, text_to_textnodes
from src.text_node import TextNode, TextType


class UtilsTest(unittest.TestCase):
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
        old_nodes = [TextNode("This is _text is invalid markdown", TextType.TEXT)]

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

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected_images = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]

        images = extract_markdown_images(text)

        self.assertListEqual(expected_images, images)

    def test_extract_markdown_images_one_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) in the middle"
        expected_images = [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]

        images = extract_markdown_images(text)

        self.assertListEqual(expected_images, images)

    def test_extract_markdown_images_no_image(self):
        text = "This is text with no image"
        expected_images = []

        images = extract_markdown_images(text)

        self.assertListEqual(expected_images, images)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected_links = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]

        links = extract_markdown_links(text)

        self.assertListEqual(expected_links, links)

    def test_extract_markdown_links_one_image(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) in the middle"
        expected_links = [("to boot dev", "https://www.boot.dev")]

        links = extract_markdown_links(text)

        self.assertListEqual(expected_links, links)

    def test_extract_markdown_links_no_image(self):
        text = "This is text with no links"
        expected_links = []

        links = extract_markdown_links(text)

        self.assertListEqual(expected_links, links)

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        expected_nodes = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ]

        actual_nodes = split_nodes_image([node])

        self.assertListEqual(expected_nodes, actual_nodes)

    def test_split_nodes_image_starts_and_ends_with_image(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        expected_nodes = [
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ]

        actual_nodes = split_nodes_image([node])

        self.assertListEqual(expected_nodes, actual_nodes)

    def test_split_nodes_image_one_image_in_the_middle(self):
        node = TextNode(
            "Text with one ![image](https://i.imgur.com/zjjcJKZ.png) in the middle",
            TextType.TEXT,
        )
        expected_nodes = [
            TextNode("Text with one ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" in the middle", TextType.TEXT),
        ]

        actual_nodes = split_nodes_image([node])

        self.assertListEqual(expected_nodes, actual_nodes)

    def test_split_nodes_image_no_image(self):
        node = TextNode("This is text without an image.", TextType.TEXT)
        expected_images = [TextNode("This is text without an image.", TextType.TEXT)]

        new_nodes = split_nodes_image([node])

        self.assertListEqual(expected_images, new_nodes)

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.html) and another [second link](https://i.imgur.com/3elNhQu.html)",
            TextType.TEXT,
        )
        expected_nodes = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.html"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.html"),
        ]

        actual_nodes = split_nodes_link([node])

        self.assertListEqual(expected_nodes, actual_nodes)

    def test_split_nodes_link_starts_and_ends_with_link(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.html) and another [second link](https://i.imgur.com/3elNhQu.html)",
            TextType.TEXT,
        )
        expected_nodes = [
            TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.html"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.html"),
        ]

        actual_nodes = split_nodes_link([node])

        self.assertListEqual(expected_nodes, actual_nodes)

    def test_split_nodes_link_one_link_in_the_middle(self):
        node = TextNode(
            "Text with one [link](https://i.imgur.com/zjjcJKZ.html) in the middle",
            TextType.TEXT,
        )
        expected_nodes = [
            TextNode("Text with one ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.html"),
            TextNode(" in the middle", TextType.TEXT),
        ]

        actual_nodes = split_nodes_link([node])

        self.assertListEqual(expected_nodes, actual_nodes)

    def test_split_nodes_link_no_link(self):
        node = TextNode("This is text without an link.", TextType.TEXT)
        expected_links = [TextNode("This is text without an link.", TextType.TEXT)]

        new_nodes = split_nodes_link([node])

        self.assertListEqual(expected_links, new_nodes)

    def test_pipeline(self):
        expected = 4

        actual = pipeline(value=1, pipes=[
            lambda x: x + 1,  # 1 + 1 = 2
            lambda x: x + 2,  # 2 + 2 = 4
        ])

        self.assertEqual(expected, actual)

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        actual_nodes = text_to_textnodes(text)

        self.assertListEqual(expected_nodes, actual_nodes)

    def test_text_to_textnodes_empty(self):
        text = ""
        expected_nodes = []

        actual_nodes = text_to_textnodes(text)

        self.assertListEqual(expected_nodes, actual_nodes)


if __name__ == '__main__':
    unittest.main()
