import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown: str) -> List[str]:
    return [block.strip() for block in markdown.split("\n\n") if block.strip()]

def block_to_block_type(markdown: str) -> BlockType:
    if markdown.startswith("#"): return BlockType.HEADING
    if markdown.startswith("```\n") and markdown.endswith("```"): return BlockType.CODE
    if all([line.startswith(">") for line in markdown.split("\n")]): return BlockType.QUOTE
    if all([line.startswith("- ") for line in markdown.split("\n")]): return BlockType.UNORDERED_LIST
    if all([bool(re.match(r"^\d+\. ", line)) for line in markdown.split("\n")]): return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH