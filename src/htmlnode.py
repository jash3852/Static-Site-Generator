class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: List[HTMLNode] = None, props: Dict[str, str] = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError()

    def props_to_html(self) -> str:
        return " " + " ".join(f'{key}="{value}"' for key, value in self.props.items()) if self.props else ""

    def __repr__(self) -> str:
        return f"{self.tag} | {self.value} | {self.children} | {self.props_to_html()}"

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: Dict[str, str] = None):
        super().__init__(tag = tag, value = value, props = props)

    def to_html(self) -> str:
        if self.value is None: raise ValueError()
        if self.tag is None: return self.value

        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self) -> str:
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: List[HTMLNode], props: Dict[str, str] = None):
        super().__init__(tag = tag, children = children, props = props)

    def to_html(self) -> str:
        if self.tag is None: raise ValueError()
        if self.children is None: raise ValueError()

        return f'<{self.tag}>{"".join([child.to_html() for child in self.children])}</{self.tag}>'