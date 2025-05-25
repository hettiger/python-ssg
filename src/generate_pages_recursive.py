import os

from generate_page import generate_page


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    if not os.path.isdir(dir_path_content):
        raise ValueError(f"Content directory {dir_path_content} does not exist")
    if not os.path.isfile(template_path):
        raise ValueError(f"Template {template_path} does not exist")
    if not os.path.isdir(dest_dir_path):
        os.makedirs(dest_dir_path)
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        if os.path.isdir(item_path):
            next_dest_dir_path = os.path.join(dest_dir_path, item)
            generate_pages_recursive(item_path, template_path, next_dest_dir_path)
        if item.endswith(".md"):
            dest_file_path = os.path.join(dest_dir_path, item[:-2] + "html")
            generate_page(item_path, template_path, dest_file_path)
