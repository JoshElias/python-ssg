from os import (
    path,
    mkdir,
    listdir,
)
from shutil import copy

def copy_files_recursive(src_path, dest_path):
    if not path.exists(src_path):
        return
    mkdir(dest_path)

    fs_objects = listdir(src_path)
    for obj in fs_objects:
        src = path.join(src_path, obj)
        dest = path.join(dest_path, obj)
        if path.isfile(src):
            copy(src, dest)
        else:
            copy_files_recursive(src, dest)
