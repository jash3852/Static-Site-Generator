from pathlib import Path

from helpers import copy_dir, generate_page, generate_pages_recursive


def main():
    copy_dir(Path("./static"), Path("./public"))
    generate_pages_recursive(Path("./content"), Path("./template.html"), Path("./public"))

if __name__ == "__main__":
    main()