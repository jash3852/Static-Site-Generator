import re
from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text: str, type: TextType, url: str = None):
        self.text = text
        self.type = type
        self.url = url

    def __eq__(self, other: TextNode) -> bool:
        return self.text == other.text and self.type == other.type and self.url == other.url

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.type.value}, {self.url})"

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0: raise Exception()

        for i, text in enumerate(split_text):
            if i % 2 == 0:
                new_nodes.append(TextNode(text, node.type, node.url))
            else:
                new_nodes.append(TextNode(text, text_type))

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    from helpers import extract_markdown_images

    new_nodes = []
    for node in old_nodes:
        split_text = [text for text in re.split(r"!\[.*?\]\(.*?\)", node.text) if text]
        extracted_images = extract_markdown_images(node.text)

        i = 0
        while i < len(split_text) or i < len(extracted_images):
            if i < len(split_text): new_nodes.append(TextNode(split_text[i], node.type, node.url))
            if i < len(extracted_images): new_nodes.append(TextNode(extracted_images[i][0], TextType.IMAGE, extracted_images[i][1]))
            i += 1

    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    from helpers import extract_markdown_links

    new_nodes = []
    for node in old_nodes:
        split_text = [text for text in re.split(r"\[.*?\]\(.*?\)", node.text) if text]
        extracted_links = extract_markdown_links(node.text)

        i = 0
        while i < len(split_text) or i < len(extracted_links):
            if i < len(split_text): new_nodes.append(TextNode(split_text[i], node.type, node.url))
            if i < len(extracted_links): new_nodes.append(TextNode(extracted_links[i][0], TextType.LINK, extracted_links[i][1]))
            i += 1

    return new_nodes

def text_to_textnodes(text: str) -> List[TextNode]:
    node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes