from os import (
    path,
    makedirs,
    listdir,
)
from pathlib import Path
from markdown_blocks import markdown_to_html_node

def extract_title(html_node):
    if html_node.tag == 'h1':
        return html_node.children[0].value
    if html_node.children != None:
        for child in html_node.children:
            result = extract_title(child)
            if result != None:
                return result

def generate_page(src_path, template_path, dest_path):
    print(f'Generating page from {src_path} to {dest_path} using {template_path}')

    if not path.exists(src_path) or not path.exists(template_path):
        raise Exception('Either source path or template does not exist')

    with open(src_path, 'r') as src_file:
        markdown = src_file.read()
    with open(template_path, 'r') as template_file:
        template = template_file.read()

    html_node = markdown_to_html_node(markdown)
    header_text = extract_title(html_node)
    if header_text is None:
        raise Exception('Html needs an h1 header')
    print(f'Found header: {header_text}')
    html_text = html_node.to_html()

    template = template.replace('{{ Title }}', header_text)
    template = template.replace('{{ Content }}', html_text)

    if not path.exists(dest_path):
        makedirs(dest_path)

    html_output_path = path.join(dest_path, 'index.html')
    with open(html_output_path, 'w') as output_file:
        output_file.write(template)

def generate_pages_recursively(dir_path_content, template_path, dest_dir_path):
    fs_objects = listdir(dir_path_content)
    for obj in fs_objects:
        content_path = path.join(dir_path_content, obj)
        if path.isfile(content_path) and Path(content_path).suffix == '.md':
            generate_page(content_path, template_path, dest_dir_path)
        else:
            next_dest_dir_path = path.join(dest_dir_path, obj)
            generate_pages_recursively(
                    content_path,
                    template_path,
                    next_dest_dir_path,
            )
