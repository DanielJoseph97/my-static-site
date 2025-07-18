from textnode import TextNode, TextType
import re
#Nested inline elements not supported (such as bold text within italic)* *-for now

def text_to_textnodes(text_string):
    #takes raw input string and converts to markdown
    bold_delim = "**"
    italic_delim = "_"
    code_delim = "`"
    nodes = [TextNode(text_string, TextType.TEXT)]
    nodes = (split_nodes_delimiter(nodes,bold_delim,TextType.BOLD))
    nodes = (split_nodes_delimiter(nodes,italic_delim,TextType.ITALIC))
    nodes = (split_nodes_delimiter(nodes, code_delim, TextType.CODE))
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
# old nodes in this case are nodes with compound text types that have to split up
# this function will split up the old nodes and return a new node with all the text types split up
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = old_node.text.split(delimiter)
        if len(split_nodes) == 1:
            # This means delimiter is not found and string returns as is
            new_nodes.append(old_node)
        elif len(split_nodes) % 2 == 0:
            # Odd number delimiter or missing a closing delimiter
            raise Exception(" invalid markdown syntax: no closing delimiter found")
        else:
            # Handling cases for one or multiple delimited text
            for i in range(len(split_nodes)):
                if i % 2 == 0:
                    # Even index (regular text or empty string)
                    if split_nodes[i] == "":
                        continue
                    new_nodes.append(TextNode(split_nodes[i], TextType.TEXT))
                else:
                    # Odd index is delimited text
                    new_nodes.append(TextNode(split_nodes[i], text_type))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        current_text = node.text
        image_props = extract_markdown_images(current_text) #list of image alt and links
        if image_props == []:
            #No image alt or links found
            new_nodes.append(node)
            continue
        for image_alt, image_link in image_props:
            section = current_text.split(f"![{image_alt}]({image_link})", 1)
            if len(section) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if section[0] != "":
                new_nodes.append(TextNode(section[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE,image_link))
            current_text = section[1]
        if current_text != "":
            new_nodes.append(TextNode(current_text,TextType.TEXT))          
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        current_text = node.text
        link_props = extract_markdown_links(current_text) #list of image alt and links
        if link_props == []:
            #No image alt or links found
            new_nodes.append(node)
            continue
        for link_alt, link_url in link_props:
            section = current_text.split(f"[{link_alt}]({link_url})", 1)
            if len(section) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if section[0] != "":
                new_nodes.append(TextNode(section[0], TextType.TEXT))
            new_nodes.append(TextNode(link_alt, TextType.LINK,link_url))
            current_text = section[1]
        if current_text != "":
            new_nodes.append(TextNode(current_text,TextType.TEXT))          
    return new_nodes

        
def extract_markdown_images(text):
    result = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return result

def extract_markdown_links(text):
    result = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return result

