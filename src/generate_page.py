import os

from extract_title import extract_title
from utils import markdown_to_html_node


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        markdown = file.read()
    with open(template_path) as file:
        template = file.read()
    title = extract_title(markdown)
    html_content = markdown_to_html_node(markdown).to_html()
    html_document = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    dest_dirpath = os.path.dirname(dest_path)
    if not os.path.isdir(dest_dirpath):
        os.makedirs(dest_dirpath)
    with open(dest_path, "w") as file:
        file.write(html_document)
