from enum import Enum
from htmlnode import *
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block):
    headings = ["# ","## ","### ","#### ","##### ","###### "]
    if any(block.startswith(h) for h in headings):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    lines = block.split("\n")
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    if all(line.startswith(f"{idx+1}. ") for idx, line in enumerate(lines)):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown): 
    blocks = markdown_to_blocks(markdown)
    # markdown doc stripped to markdown blocks
    blocks_html_nodes = []
    for block in blocks:
        # for each block, determine type of block with block type function
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                block_single_line = block.replace('\n',' ')
                block_node = ParentNode("p",text_to_children(block_single_line))
                blocks_html_nodes.append(block_node)

            case BlockType.HEADING:
                block = block.replace('\n',' ')
                h_count = 0
                while h_count < len(block) and block[h_count] == "#":
                    h_count += 1
                heading_text = block[h_count:].strip()
                block_node = ParentNode(f"h{h_count}",text_to_children(heading_text))
                blocks_html_nodes.append(block_node)

            case BlockType.CODE:
                
                code_text = extract_code_from_text(block)
                code_node = LeafNode("code",code_text)
                pre_node = ParentNode("pre",[code_node])
                blocks_html_nodes.append(pre_node)

            case BlockType.QUOTE:
                lines = block.split("\n")
                stripped_lines = [line.lstrip("> ").rstrip() for line in lines]
                quote_text = "\n".join(stripped_lines).strip()
                block_node = ParentNode("blockquote",text_to_children(quote_text))
                blocks_html_nodes.append(block_node)

            case BlockType.UNORDERED_LIST:
                lines = block.split("\n")
                li_nodes = []
                for line in lines:
                    stripped = line.lstrip()
                    if stripped.startswith("- "):
                        item_text = stripped[2:].strip()
                        li_node = ParentNode("li",text_to_children(item_text))
                        li_nodes.append(li_node)
                block_node = ParentNode("ul", li_nodes)
                blocks_html_nodes.append(block_node)

            case BlockType.ORDERED_LIST:
                lines = block.split("\n")
                ol_nodes = []
                for line in lines:
                    stripped = line.lstrip()
                    number_end = 0
                    # Find the first period after a series of digits
                    while number_end < len(stripped) and stripped[number_end].isdigit():
                        number_end += 1
                    if number_end < len(stripped) and stripped[number_end] == '.':
                        # Skip the dot and the space if it's there
                        item_text = stripped[number_end+1:].lstrip()
                    else:
                        # Fallback if line doesn't match expected "1. " pattern
                        item_text = stripped
                    ol_node = ParentNode("li", text_to_children(item_text))
                    ol_nodes.append(ol_node)

                block_node = ParentNode("ol", ol_nodes)
                blocks_html_nodes.append(block_node)

    # Parent all child nodes under single parent with corresponding block type
    parent_block = ParentNode("div", blocks_html_nodes)
    return parent_block
        
def text_to_children(text):
    # Take a text (block) and return HTML nodes (inline markdown)
    block_text_nodes = text_to_textnodes(text) #output is list of TextNodes
    block_html_nodes = []
    for nodes in block_text_nodes:
        block_html_nodes.append(text_node_to_html_node(nodes)) #output is corresponding list of HTML Nodes
    return block_html_nodes

def extract_code_from_text(text):
    #removes ``` from code block
    lines = text.split("\n")
    code_lines = lines[1:-1]
    code_text = "\n".join(code_lines) + "\n"
    return code_text
    


    