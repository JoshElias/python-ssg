from os import path
from shutil import rmtree
from file_utils import copy_files_recursive
from ssg import generate_pages_recursively 

project_path = '/home/josh/Projects/python-ssg'
public_path = path.join(project_path, 'public')
static_path = path.join(project_path, 'static')

def main():
    if path.exists(public_path):
        rmtree(public_path)

    copy_files_recursive(static_path, public_path)
    template_path = path.join(project_path, 'template.html')
    content_path = path.join(project_path, 'content')
    generate_pages_recursively(
        content_path,
        template_path,
        public_path
    )

main()
