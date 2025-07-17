from textnode import TextNode, TextType
import re
#Nested inline elements not supported (such as bold text within italic)* *-for now

def split_nodes_delimiter(old_nodes, delimiter, text_type):
# old nodes in this case are nodes with compound text types that have to split up
# this function will split up the old nodes and return a new node with all the text types split up
    new_node = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_node.append(old_node)
            continue
        split_nodes = old_node.text.split(delimiter)
        if len(split_nodes) == 1:
            # This means delimiter is not found and string returns as is
            new_node.append(old_node)
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
                    new_node.append(TextNode(split_nodes[i], TextType.TEXT))
                else:
                    # Odd index is delimited text
                    new_node.append(TextNode(split_nodes[i], text_type))
    return new_node

def extract_markdown_images(text):
    result = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return result

def extract_markdown_links(text):
    result = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return result

def split_nodes_image(old_nodes):
    new_node = []
    for node in old_nodes:
        image_props = extract_markdown_images(node.text) #list of image alt and links
        if image_props == []:
            #No image alt or links found
            new_node.append(node)
        else:
            for image_alt, image_link in list(image_props):
                section = node.text.split(f"![{image_alt}]({image_link})", 1)
                new_node.append(TextNode(section[0],TextType.TEXT))
                new_node.append(TextNode(image_alt, TextType.IMAGE, image_link))
                new_node.append(TextNode(section[1],TextType.TEXT))            
    return new_node


def split_nodes_link(old_nodes):
    new_node = []
    for node in old_nodes:
        image_props = extract_markdown_links(node.text) #list of image alt and links
        if len(image_props) == 1:
            #No image alt or links found
            new_node.append(node)
        else:
            for link_alt, link_url in list(image_props):
                section = node.text.split(f"![{link_alt}]({link_url})", 1)
                new_node.append(TextNode(section[0],TextType.TEXT))
                new_node.append(tuple(link_alt, link_url))
    return new_node