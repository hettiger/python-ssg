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
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
