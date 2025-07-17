import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_props(self):
        props = {"href": "https://www.google.com", "target": "_blank"}
        node = HTMLNode("a", "Click me", None, props)
        result = node.props_to_html()
        # Test that it contains the expected attribute
        self.assertIn(' href="https://www.google.com"', result)
        self.assertIn(' target="_blank"', result)

    def test_props_to_html_no_props(self):
        node = HTMLNode("p", "Hello", None, None)
        result = node.props_to_html()
        self.assertEqual(result, "")

    def test_repr(self):
        node = HTMLNode("p", "Hello world", None, {"class": "greeting"})
        result = repr(node)
        # Check that the string representation contains the expected information
        self.assertIn("p", result)
        self.assertIn("Hello world", result)
        self.assertIn("class", result)
        self.assertIn("greeting", result)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
       node = LeafNode("p", "Hello World!")
       self.assertEqual(node.to_html(), "<p>Hello World!</p>")

    def test_leafnode_no_value_raises(self):
        with self.assertRaises(ValueError):
            node = LeafNode("p", None)
            node.to_html()

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b","grandchild")
        child_node = ParentNode("span",[grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")
    
    def test_to_html_with_multiple_children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("b", "child2")
        parent_node = ParentNode("div",[child_node1, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child1</span><b>child2</b></div>")
    
    def test_to_html_no_children_raises(self):
        with self.assertRaises(ValueError):
            node = ParentNode("div", None)
            node.to_html()

