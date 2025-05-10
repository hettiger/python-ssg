from collections.abc import Generator

from src.html_node import HTMLNode, LeafNode
from src.text_node import TextNode, TextType
from itertools import chain


def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Invalid text type: {text_node.text_type}")


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    def split_node_delimiter(node: TextNode) -> Generator[TextNode, None, None]:
        d_len = len(delimiter)
        start = str.find(node.text, delimiter, 0)
        end = str.find(node.text, delimiter, start + d_len) + d_len
        preceding_text = node.text[0:start]
        matching_text = node.text[start+d_len:end-d_len]
        following_text = node.text[end:]

        if start == -1:  # No match, we're done!
            yield node
            return

        if preceding_text:
            yield TextNode(preceding_text, node.text_type)

        if matching_text:
            yield TextNode(matching_text, text_type)

        if following_text:
            yield from split_node_delimiter(TextNode(following_text, node.text_type))

    return list(chain(*[split_node_delimiter(old_node) for old_node in old_nodes]))
