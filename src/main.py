from base_path import base_path
from copy_contents import copy_contents


def main():
    copy_contents(base_path("static"), base_path("public"))


if __name__ == "__main__":
    main()