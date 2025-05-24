import re
from typing import Callable
from itertools import chain

from block_type import BlockType
from html_node import HTMLNode, LeafNode, ParentNode
from text_node import TextNode, TextType


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
    return _split_nodes(
        old_nodes=old_nodes,
        extract=extract_markdown_images,
        delimiter=lambda text, url: f"![{text}]({url})",
        text_type=TextType.IMAGE
    )


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return _split_nodes(
        old_nodes=old_nodes,
        extract=extract_markdown_links,
        delimiter=lambda text, url: f"[{text}]({url})",
        text_type=TextType.LINK
    )


def _split_nodes(
    old_nodes: list[TextNode],
    extract: Callable[[str], list[tuple[str, str]]],
    delimiter: Callable[[str, str], str],
    text_type: TextType
) -> list[TextNode]:
    def split_node(node: TextNode) -> list[TextNode]:
        if node.text_type != TextType.TEXT:
            return [node]

        items = extract(node.text)

        if not items:
            return [node]

        nodes = []
        text_unprocessed = node.text

        for item_text, item_url in items:
            text_item = delimiter(item_text, item_url)
            [text_before, text_after] = text_unprocessed.split(text_item, maxsplit=1)
            if text_before:
                nodes.append(TextNode(text_before, TextType.TEXT))
            nodes.append(TextNode(text=item_text, text_type=text_type, url=item_url))
            text_unprocessed = text_after

        if text_unprocessed:
            nodes.append(TextNode(text_unprocessed, TextType.TEXT))

        return nodes

    return list(chain.from_iterable(map(split_node, old_nodes)))


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text=text, text_type=TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(markdown: str) -> list[str]:
    return list(filter(lambda block: block != "", map(lambda block: block.strip(), markdown.split("\n\n"))))


def block_to_block_type(block: str) -> BlockType:
    if is_heading_block(block):
        return BlockType.HEADING
    if is_code_block(block):
        return BlockType.CODE
    if is_quote_block(block):
        return BlockType.QUOTE
    if is_unordered_list_block(block):
        return BlockType.UNORDERED_LIST
    if is_ordered_list_block(block):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def is_heading_block(block: str) -> bool:
    return bool(re.match(r"^#{1,6} ", block))


def is_code_block(block: str) -> bool:
    lines = block.splitlines()
    if len(lines) < 3:
        return False
    return lines[0] == "```" and lines[-1] == "```"


def is_quote_block(block: str) -> bool:
    for line in block.splitlines():
        if not line.startswith(">"):
            return False
    return True


def is_unordered_list_block(block: str) -> bool:
    for line in block.splitlines():
        if not line.startswith("- "):
            return False
    return True


def is_ordered_list_block(block: str) -> bool:
    number = 1
    for line in block.splitlines():
        if not line.startswith(f"{number}. "):
            return False
        number += 1
    return True


def markdown_to_html_node(markdown: str) -> HTMLNode:
    root_node = HTMLNode(tag="div", children=[])
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                html_node = heading_block_to_html_node(block)
            case BlockType.CODE:
                html_node = code_block_to_html_node(block)
            case BlockType.QUOTE:
                html_node = quote_block_to_html_node(block)
            case BlockType.UNORDERED_LIST:
                html_node = unordered_list_block_to_html_node(block)
            case BlockType.ORDERED_LIST:
                html_node = ordered_list_block_to_html_node(block)
            case _:
                html_node = paragraph_block_to_html_node(block)
        root_node.children.append(html_node)
    return root_node


def heading_block_to_html_node(block: str) -> HTMLNode:
    heading_level = len(re.match(r"^(#{1,6}) ", block).group(1))
    heading_text = block[heading_level + 1:]
    children = text_to_children(heading_text)
    if len(children) == 1:
        return LeafNode(tag=f"h{heading_level}", value=heading_text)
    return ParentNode(tag=f"h{heading_level}", children=children)


def code_block_to_html_node(block: str) -> HTMLNode:
    lines = block.splitlines()
    text = "\n".join(lines[1:-1])+"\n"
    text_node = TextNode(text=text, text_type=TextType.CODE)
    return ParentNode(tag="pre", children=[text_node_to_html_node(text_node)])


def quote_block_to_html_node(block: str) -> HTMLNode:
    lines = []
    for line in block.splitlines():
        matches = re.match(r"^>\s*(\S+.*)$", line)
        if not matches:
            continue
        lines.append(matches.group(1))
    text = " ".join(lines)
    children = text_to_children(text)
    if len(children) == 1:
        return LeafNode(tag="blockquote", value=text)
    return ParentNode(tag="blockquote", children=children)


def unordered_list_block_to_html_node(block: str) -> HTMLNode:
    unordered_list = ParentNode(tag="ul", children=[])
    list_items = []
    for line in block.splitlines():
        list_items.append(re.match(r"^- (.*)$", line).group(1))
    for text in list_items:
        children = text_to_children(text)
        unordered_list.children.append(ParentNode(tag="li", children=children))
    return unordered_list


def ordered_list_block_to_html_node(block: str) -> HTMLNode:
    ordered_list = ParentNode(tag="ol", children=[])
    list_items = []
    for line in block.splitlines():
        list_items.append(re.match(r"^\d+\. (.*)$", line).group(1))
    for text in list_items:
        children = text_to_children(text)
        if len(children) == 1:
            ordered_list.children.append(LeafNode(tag="li", value=text))
        else:
            ordered_list.children.append(ParentNode(tag="li", children=children))
    return ordered_list


def paragraph_block_to_html_node(block: str) -> HTMLNode:
    children = text_to_children(block.replace("\n", " "))
    return ParentNode(tag="p", children=children)


def text_to_children(text: str) -> list[HTMLNode]:
    nodes = text_to_textnodes(text)
    return list(map(text_node_to_html_node, nodes))
