from htmlnode import ParentNode 
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

block_type_paragraph = 'paragraph'
block_type_heading = 'heading'
block_type_code = 'code'
block_type_quote = 'quote'
block_type_ulist = 'unordered_list'
block_type_olist = 'ordered_list'

def markdown_to_html_node(md):
    blocks = markdown_to_blocks(md)
    child_nodes = []
    for b in blocks:
        child_nodes.append(block_to_html_node(b))
    return ParentNode('div', child_nodes, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return paragraph_to_html_node(block)
    if block_type == block_type_heading:
        return heading_to_html_node(block)
    if block_type == block_type_code:
        return code_to_html_node(block)
    if block_type == block_type_quote:
        return quote_to_html_node(block)
    if block_type == block_type_ulist:
        return ulist_to_html_node(block)
    if block_type == block_type_olist:
        return olist_to_html_node(block)
    raise ValueError('Invalid block type')

def is_header_block(text):
    print('test')

def block_to_block_type(block):
    lines = block.split("\n")

    if (
        block.startswith("# ")
        or block.startswith("## ")
        or block.startswith("### ")
        or block.startswith("#### ")
        or block.startswith("##### ")
        or block.startswith("###### ")
    ):
        return block_type_heading
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return block_type_code
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return block_type_paragraph
        return block_type_quote
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return block_type_paragraph
        return block_type_ulist
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return block_type_paragraph
        return block_type_ulist
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return block_type_paragraph
            i += 1
        return block_type_olist
    return block_type_paragraph

def markdown_to_blocks(md):
    blocks = md.split('\n\n')
    blocks = map(lambda b: b.strip(), blocks)
    blocks = filter(lambda b: len(b) > 0, blocks)
    return list(blocks)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    child_nodes = []
    for n in text_nodes:
        child = text_node_to_html_node(n)
        child_nodes.append(child)
    return child_nodes

def paragraph_to_html_node(block):
    lines = block.split('\n')
    paragraph = ' '.join(lines)
    child_nodes = text_to_children(paragraph)
    return ParentNode('p', child_nodes)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == '#':
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError('Empty header')
    if level > 6:
        raise ValueError('Invalid header level')
    text = block[level+1:]
    child_nodes = text_to_children(text)
    return ParentNode(f'h{level}', child_nodes) 

def code_to_html_node(block):
    text = block[4:-3]
    child_nodes = text_to_children(text)
    code = ParentNode('code', child_nodes)
    return ParentNode('pre', [code])

def quote_to_html_node(block):
    lines = block.split('\n')
    new_lines = []
    for line in lines:
        new_lines.append(line.lstrip('>').strip())
    text = ' '.join(new_lines)
    child_nodes = text_to_children(text)
    return ParentNode('blockquote', child_nodes)


def ulist_to_html_node(block):
    lines = block.split('\n')
    list_items = []
    for line in lines:
        text = line[2:]
        child_nodes = text_to_children(text)
        list_items.append(ParentNode('li', child_nodes))
    return ParentNode('ul', list_items)

def olist_to_html_node(block):
    lines = block.split('\n')
    list_items = []
    for line in lines:
        text = line[3:]
        child_nodes = text_to_children(text)
        list_items.append(ParentNode('li', child_nodes))
    return ParentNode('ol', list_items)
