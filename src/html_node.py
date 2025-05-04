from functools import reduce


class HTMLNode:
    def __init__(
        self,
        tag: str = None,
        value: str = None,
        children: list['HTMLNode'] = None,
        props: dict[str, str] = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""
        return reduce(
            lambda html, prop: f"{html} {prop[0]}=\"{prop[1]}\"",
            list(self.props.items()),
            "",
        )

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: None|str,
        value: None|str,
        props: dict[str, str] = None,
    ):
        if value is None:
            raise ValueError("All leaf nodes must have a value.")
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: None|str,
        children: None|list[HTMLNode],
        props: dict[str, str] = None,
    ):
        if tag is None:
            raise ValueError("All parent nodes must have a tag.")
        if children is None:
            raise ValueError("All parent nodes must have children.")
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if isinstance(self, LeafNode):
            return self.to_html()
        content = reduce(lambda html, child: f"{html}{child.to_html()}", self.children, "")
        return f"<{self.tag}{self.props_to_html()}>{content}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"