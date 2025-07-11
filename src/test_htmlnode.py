import unittest

from htmlnode import HTMLNode

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

    