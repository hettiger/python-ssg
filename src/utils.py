import re

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
    def split_node(node: TextNode) -> list[TextNode]:
        if node.text_type != TextType.TEXT:
            return [node]

        nodes = []
        sections = node.text.split(delimiter)
        n_sections = len(sections)

        if n_sections % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")

        for i in range(n_sections):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                nodes.append(TextNode(sections[i], text_type))

        return nodes

    return list(chain.from_iterable(map(split_node, old_nodes)))


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^]]+)]\(([^)]+)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"\[([^]]+)]\(([^)]+)\)", text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    def split_node(node: TextNode) -> list[TextNode]:
        if node.text_type != TextType.TEXT:
            return [node]

        images = extract_markdown_images(node.text)

        if not images:
            return [node]

        nodes = []
        text_unprocessed = node.text

        for image_alt, image_url in images:
            text_image = f"![{image_alt}]({image_url})"
            [text_before, text_after] = text_unprocessed.split(text_image, maxsplit=1)
            if text_before:
                nodes.append(TextNode(text_before, TextType.TEXT))
            nodes.append(TextNode(text=image_alt, text_type=TextType.IMAGE, url=image_url))
            text_unprocessed = text_after

        if text_unprocessed:
            nodes.append(TextNode(text_unprocessed, TextType.TEXT))

        return nodes

    return list(chain.from_iterable(map(split_node, old_nodes)))


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    def split_node(node: TextNode) -> list[TextNode]:
        if node.text_type != TextType.TEXT:
            return [node]

        links = extract_markdown_links(node.text)

        if not links:
            return [node]

        nodes = []
        text_unprocessed = node.text

        for link_text, link_url in links:
            text_link = f"[{link_text}]({link_url})"
            [text_before, text_after] = text_unprocessed.split(text_link, maxsplit=1)
            if text_before:
                nodes.append(TextNode(text_before, TextType.TEXT))
            nodes.append(TextNode(text=link_text, text_type=TextType.LINK, url=link_url))
            text_unprocessed = text_after

        if text_unprocessed:
            nodes.append(TextNode(text_unprocessed, TextType.TEXT))

        return nodes

    return list(chain.from_iterable(map(split_node, old_nodes)))
