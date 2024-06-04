from htmlnode import LeafNode

text_type_text      = "text"
text_type_bold      = "bold"
text_type_italic    = "italic"
text_type_code      = "code"
text_type_link      = "link"
text_type_image     = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
        
    def __eq__(self, other):
        return (
            self.text == other.text 
            and self.text_type == other.text_type
            and self.url == other.url
        )
    
    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type}, {self.url})'

def text_node_to_html_node(text_node):
    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.text)
    if text_node.text_type == text_type_bold:
        return LeafNode('b', text_node.text)
    if text_node.text_type == text_type_italic:
        return LeafNode('i', text_node.text)
    if text_node.text_type == text_type_code:
        return LeafNode('code', text_node.text)
    if text_node.text_type == text_type_link:
        return LeafNode('a', text_node.text, {'href': text_node.url})
    if text_node.text_type == text_type_image:
        return LeafNode('img', '', {'src': text_node.url, 'alt': text_node.text})
    raise ValueError(f"Invalid text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):

    def find_subnodes_by_delimiter(text, is_delimiter_open, nodes):
        try:
            index = text.index(delimiter)
            if not is_delimiter_open:
                text = text[1:]
            if is_delimiter_open:
                nodes.append(TextNode(text[1:index], text_type))
                text = text[index:]
            if len(text) > 1:
                return nodes

            is_delimiter_open = not is_delimiter_open

        except ValueError:
            if is_delimiter_open:
                raise Exception(f'Found mismatching delimiter: {delimiter}')
            return nodes 
        
        return find_subnodes_by_delimiter(text, is_delimiter_open, nodes)
        
    new_nodes = []
    for node in old_nodes:
        if node is not TextNode:
            new_nodes.append(node)
            continue
        
        new_nodes.extend(find_subnodes_by_delimiter(node.text, False, []))
    return new_nodes
                   
            

