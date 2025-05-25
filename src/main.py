from base_path import base_path
from copy_contents import copy_contents
from generate_pages_recursive import generate_pages_recursive


def main():
    copy_contents(base_path("static"), base_path("public"))

    generate_pages_recursive(
        dir_path_content=base_path("content"),
        template_path=base_path("template.html"),
        dest_dir_path=base_path("public")
    )


if __name__ == "__main__":
    main()