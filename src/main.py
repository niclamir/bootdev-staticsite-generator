from textnode import *
from htmlnode import *
from inline_markdown import *

def main():

    # Clean up public and copy from static
    copy_src_to_public("static/","public/")

    # Generate pages recursively from template
    generate_page_recursively("content/", "template.html", "public/")

if __name__ == '__main__':
    main()