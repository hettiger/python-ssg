from base_path import base_path
from copy_contents import copy_contents
from generate_page import generate_page


def main():
    copy_contents(base_path("static"), base_path("public"))

    generate_page(
        from_path=base_path("content/index.md"),
        template_path=base_path("template.html"),
        dest_path=base_path("public/index.html")
    )


if __name__ == "__main__":
    main()