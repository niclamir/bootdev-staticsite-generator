import sys
from textnode import *
from htmlnode import *
from inline_markdown import *

def main():

    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    # Clean up public and copy from static
    copy_src_to_public("static/","docs/")

    # Generate pages recursively from template
    generate_page_recursively("content/", "template.html", "docs/", basepath)

if __name__ == '__main__':
    main()