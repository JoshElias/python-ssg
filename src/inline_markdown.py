import re

from textnode import (
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
    TextNode,
)

def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, '**', text_type_bold)
    nodes = split_nodes_delimiter(nodes, '*', text_type_italic)
    nodes = split_nodes_delimiter(nodes, '`', text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):

    def find_subnodes_by_delimiter(text, is_delimiter_open, nodes):
        try:
            index = text.index(delimiter)
        except ValueError:
            if is_delimiter_open:
                raise Exception(f'Found mismatching delimiter: {delimiter}')
            new_node = TextNode(text, text_type_text)
            nodes.append(new_node)
            return nodes 

        new_node = TextNode(text[:index], text_type if is_delimiter_open else text_type_text)
        nodes.append(new_node)
        text = text[index+len(delimiter):]

        if len(text) < 1:
            return nodes

        is_delimiter_open = not is_delimiter_open
        return find_subnodes_by_delimiter(text, is_delimiter_open, nodes)
        
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not text_type_text:
            new_nodes.append(node)
            continue
        
        new_nodes.extend(find_subnodes_by_delimiter(node.text, False, []))
    return new_nodes
                   
            
def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not text_type_text:
            new_nodes.append(node)
            continue
        els = extract_markdown_images(node.text)
        
        if len(els) < 1:
            new_nodes.append(node)
            continue
        
        original_text = node.text
        for el in els:
            beginning = f'![{el[0]}]({el[1]})'
            slice = original_text.split(beginning, 1)
            if len(slice) != 2:
                raise Exception('Invalid markdown, image section not closed')
            if len(slice[0]) > 0:
                new_nodes.append(TextNode(slice[0], text_type_text))
            new_nodes.append(TextNode(el[0], text_type_image, el[1]))
            original_text = slice[1]
        if len(original_text) > 0:
            new_nodes.append(TextNode(original_text, text_type_text))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not text_type_text:
            new_nodes.append(node)
            continue
        els = extract_markdown_links(node.text)
        
        if len(els) < 1:
            new_nodes.append(node)
            continue
        
        original_text = node.text
        for el in els:
            beginning = f'[{el[0]}]({el[1]})'
            slice = original_text.split(beginning, 1)
            if len(slice) != 2:
                raise Exception('Invalid markdown, link section not closed')
            if len(slice[0]) > 0:
                new_nodes.append(TextNode(slice[0], text_type_text))
            new_nodes.append(TextNode(el[0], text_type_link, el[1]))
            original_text = slice[1]
        if len(original_text) > 0:
            new_nodes.append(TextNode(original_text, text_type_text))

    return new_nodes
