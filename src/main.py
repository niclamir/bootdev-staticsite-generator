from textnode import *
from htmlnode import *
from inline_markdown import *

def main():

    # Clean up public and copy from static
    copy_src_to_public("static/","public/")

    # Generate page from template
    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == '__main__':
    main()