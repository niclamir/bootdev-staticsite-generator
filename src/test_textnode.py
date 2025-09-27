import unittest
from textnode import *
from htmlnode import *

class TestTextNode(unittest.TestCase):
    
    def test_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url_none(self):
        node = TextNode("url should be none", TextType.BOLD)
        self.assertEqual(node.url, None)
    
    def test_texttype_mismatch(self):
        node = TextNode("bold type", TextType.BOLD)
        node2 = TextNode("link type", TextType.LINK)
        self.assertNotEqual(node, node2)
    
    def test_properties_different(self):
        node = TextNode("same", TextType.BOLD)
        node2 = TextNode("same", TextType.BOLD, "url defined")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()