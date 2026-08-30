import os
import re
import shutil
from pathlib import Path

from block import markdown_to_blocks, block_to_block_type, BlockType
from htmlnode import LeafNode, ParentNode
from textnode import TextType, TextNode, text_to_textnodes


def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    match text_node.type:
        case TextType.TEXT: return LeafNode(tag = None, value = text_node.text)
        case TextType.BOLD: return LeafNode(tag = "b", value = text_node.text)
        case TextType.ITALIC: return LeafNode(tag = "i", value = text_node.text)
        case TextType.CODE: return LeafNode(tag = "code", value = text_node.text)
        case TextType.LINK: return LeafNode(tag = "a", value = text_node.text, props = { "href": text_node.url })
        case TextType.IMAGE: return LeafNode(tag = "img", value = "", props = { "src": text_node.url, "alt": text_node.text })
        case _: raise Exception()

def markdown_to_html_node(markdown: str) -> HTMLNode:
    parent_node = ParentNode("div", [])
    for block in markdown_to_blocks(markdown):
        match block_to_block_type(block):
            case BlockType.PARAGRAPH:
                parent_node.children.append(ParentNode("p", text_to_children(block.replace("\n", " "))))
            case BlockType.HEADING:
                num_heading = block.count("#")
                last_heading_index = block.rfind("#")
                heading_text = block[last_heading_index + 2:]
                parent_node.children.append(LeafNode(f"h{num_heading}", heading_text))
            case BlockType.CODE:
                parent_node.children.append(ParentNode("pre", [text_node_to_html_node(TextNode(block.replace("```\n", "").replace("```", ""), TextType.CODE))]))
            case BlockType.QUOTE:
                parent_node.children.append(LeafNode("blockquote", "\n".join([line.replace(">", "").strip() for line in block.split("\n")])))
            case BlockType.UNORDERED_LIST:
                parent_node.children.append(ParentNode("ul", [ParentNode("li", text_to_children(line[2:])) for line in block.split("\n")]))
            case BlockType.ORDERED_LIST:
                parent_node.children.append(ParentNode("ol", [ParentNode("li", text_to_children(line[3:])) for line in block.split("\n")]))

    return parent_node

def text_to_children(text: str) -> List[HTMLNode]:
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]

def extract_markdown_images(text: str) -> List[Tuple[str, str]]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def copy_dir(source: Path, destination: Path) -> None:
    if not os.path.exists(source): raise Exception("Source path not found")
    if not os.path.exists(destination): os.mkdir(destination)

    # Delete all from destination path
    for item in destination.iterdir():
        if item.is_file() or item.is_symlink(): item.unlink()
        elif item.is_dir(): shutil.rmtree(item)

    shutil.copytree(source, destination, dirs_exist_ok = True)

def extract_title(markdown: str) -> str:
    for line in markdown.split("\n"):
        if line.startswith("#"): return line[2:].strip()

    raise Exception()

def generate_page(from_path: Path, template_path: Path, dest_path: Path, basepath: Path) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f: content = f.read()
    with open(template_path, "r") as f: template = f.read()

    html = markdown_to_html_node(content).to_html()
    title = extract_title(content)
    template = template.replace("{{ Title }}", title).replace("{{ Content }}", html).replace('href="/', f'href="{basepath}/').replace('src="/', f'src="{basepath}/')

    dest_path.parent.mkdir(parents = True, exist_ok = True)
    dest_path.write_text(template)

def generate_pages_recursive(dir_path_content: Path, template_path: Path, dest_dir_path: Path, basepath: Path) -> None:
    for item in dir_path_content.iterdir():
        if item.is_file() and item.name.endswith(".md"):
            generate_page(dir_path_content / item.name, template_path, dest_dir_path / item.name.replace(".md", ".html"), basepath)
        elif item.is_dir():
            generate_pages_recursive(dir_path_content / item.name, template_path, dest_dir_path / item.name, basepath)
