import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    
    def test_eq(self):
        node = HTMLNode("h1", "This is a text", [], {})
        node2 = HTMLNode("h1", "This is a text", [], {})
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = HTMLNode("h1", "This is a text", [], {})
        node2 = HTMLNode("h2", "This is a different text", [1, 2], {})
        self.assertNotEqual(node, node2)

    def test_props_to_html(self):
        control_str = 'href="https://www.google.com" target="_blank"'
        props = {"href": "https://www.google.com","target": "_blank",}
        node = HTMLNode("tag", "", [], props)
        result = node.props_to_html()
        self.assertEqual(result, control_str)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Bold Text!")
        self.assertEqual(node.to_html(), "<b>Bold Text!</b>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), f'<a href=\"https://www.google.com\">Click me!</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()