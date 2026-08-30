from pathlib import Path
import sys

from helpers import copy_dir, generate_page, generate_pages_recursive


def main():
    copy_dir(Path("./static"), Path("./docs"))
    generate_pages_recursive(Path("./content"), Path("./template.html"), Path("./docs"), Path(sys.argv[1] if len(sys.argv) >= 2 else "/"))

if __name__ == "__main__":
    main()