import re
import os
import shutil
from textnode import *
from htmlnode import *

def text_node_to_html_node(text_node):
    
    match text_node.text_type:

        case TextType.TEXT:
            new_leaf_node = LeafNode(None,text_node.text)

        case TextType.BOLD:
            new_leaf_node = LeafNode("b",text_node.text)

        case TextType.ITALIC:
            new_leaf_node = LeafNode("i",text_node.text)

        case TextType.CODE:
            new_leaf_node = LeafNode("code",text_node.text)

        case TextType.LINK:
            new_leaf_node = LeafNode("a",text_node.text,{"href": text_node.url})

        case TextType.IMAGE:
            if text_node.url is None:
                raise ValueError(f"Missing URL")
            new_leaf_node = LeafNode("img","",{"src": text_node.url,"alt": text_node.text})

        case _:
            raise ValueError(f"'{text_node.text_type}' is NOT in the TextType enum values.")

    return new_leaf_node

def split_nodes_delimiter(old_nodes, delimiter, text_type):

    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            split_text = old_node.text.split(delimiter)

            if len(split_text) % 2 == 0:
                raise ValueError("unmatched delimiter")
            
            for i, section in enumerate(split_text):
                if i % 2 == 0:
                    new_nodes.append(TextNode(section, TextType.TEXT))
                elif i % 2 != 0:
                    new_nodes.append(TextNode(section, text_type))
                
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    
    new_nodes = []

    for old_node in old_nodes:
        
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            remaining = old_node.text
            matches = extract_markdown_images(remaining)

            if not matches:
                new_nodes.append(old_node)
            else:

                for alt, url in matches:
                    token = f"![{alt}]({url})"
                    parts = remaining.split(token, 1)
                    before = parts[0]
                    after = parts[1]

                    if before:
                        new_nodes.append(TextNode(before,TextType.TEXT))
                    new_nodes.append(TextNode(alt, TextType.IMAGE, url))
                    remaining = after
                if remaining:
                    new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            remaining = old_node.text
            matches = extract_markdown_links(remaining)

            if not matches:
                new_nodes.append(old_node)
            else:

                for alt, url in matches:
                    token = f"[{alt}]({url})"
                    parts = remaining.split(token, 1)
                    before = parts[0]
                    after = parts[1]

                    if before:
                        new_nodes.append(TextNode(before,TextType.TEXT))
                    new_nodes.append(TextNode(alt, TextType.LINK, url))
                    remaining = after
                if remaining:
                    new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):

    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes

def markdown_to_blocks(markdown):

    blocks = []

    if markdown != "":
            parts = markdown.split("\n\n")

            for part in parts:
                part = part.strip()
                if part != "":
                    blocks.append(part)

    return blocks

def block_to_block_type(markdown):

    check_headings_block = re.findall(r"^#{1,6}", markdown)
    check_code_block = re.findall(r"^```[\s\S]*?```$", markdown)
    check_quote_block = re.findall(r"^\>", markdown)
    check_unordered_list_block = re.findall(r"^- ", markdown)
    check_ordered_list_block = re.findall(r"^(\d+)\. ", markdown)

    if check_headings_block:
        return BlockType.HEADING
    elif check_code_block:
        return BlockType.CODE
    elif check_quote_block:
        return BlockType.QUOTE
    elif check_unordered_list_block:
        return BlockType.ULIST
    elif check_ordered_list_block:
        return BlockType.OLIST
    else:
        return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def copy_src_to_public(src_dir, dst_dir):

    # Make sure the initial directories exist
    if not os.path.exists(src_dir):
        raise FileExistsError(f"{src_dir} path does not exist!")

    # Clean up destination if it exists
    if os.path.exists(dst_dir):
        shutil.rmtree(dst_dir)

    # Recreate destination directory
    os.mkdir(dst_dir)

    # Finally, copy all files and directories recursively
    copy_dir(src_dir, dst_dir)

def copy_dir(src_dir, dst_dir):

    # Iterate over source path
    for file in os.listdir(src_dir):
        
        # If path is a file, copy to destination
        if os.path.isfile(src_dir + file):
            shutil.copy(src_dir + file, dst_dir)
        else:
            # Else, recurse into the source dir
            copy_src_to_public(src_dir + file + "/", dst_dir + file + "/")

def extract_title(markdown):

    if not re.findall(r"^# ",markdown):
        raise ValueError("H1 Header not found!")
    else:
        return markdown.split("\n")[0][1:].strip()
    
def generate_page(from_path, template_path, dest_path):

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    try:
        with open(from_path, 'r') as file:
            markdown_file = file.read()
            file.close()
    except FileNotFoundError:
        print(f"Error: file '{from_path}' not found!")

    try:
        with open(template_path, 'r') as file:
            template_file = file.read()
            file.close()
    except FileNotFoundError:
        print(f"Error: file '{from_path}' not found!")

    html_str = markdown_to_html_node(markdown_file).to_html()
    title = extract_title(markdown_file)

    # Add Title
    template_file = template_file.replace("{{ Title }}",title)
    # Add Content
    template_file = template_file.replace("{{ Content }}", html_str)

    # Write to destination path making sure directory exists
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))

    with open(dest_path,"w") as file:
        file.write(template_file)
        file.close()
    
# Some standard library docs that might be helpful:

# open
# .read()
# .close()
# .replace()
# os.path.dirname
# os.makedirs
# .startswith()
# .split()




