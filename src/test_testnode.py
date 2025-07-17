import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
	def test_eq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.BOLD)
		self.assertEqual(node, node2)
	
	def test_noteq(self):
		node = TextNode("This is a text node", TextType.TEXT)
		node2 = TextNode("This is a text node", TextType.ITALIC)
		self.assertNotEqual(node, node2)
	
	def test_noteq_different_text(self):
		node = TextNode("This is one text type", TextType.TEXT)
		node2 = TextNode("This is another text type", TextType.TEXT)
		self.assertNotEqual(node, node2)

	def test_eq_url(self):
		node = TextNode("Some text", TextType.TEXT, url=None)
		node2 = TextNode("Some text", TextType.TEXT, url=None)
		self.assertEqual(node, node2)
	
	def test_repr(self):
		node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
		self.assertEqual("TextNode(This is a text node, text, https://www.boot.dev)",repr(node))

class TestTextNodetoHTMLNode(unittest.TestCase):
	def test_text(self):
		node = TextNode("This is a text node", TextType.TEXT)
		html_node = text_node_to_html_node(node) 
		self.assertEqual(html_node.tag, None)
		self.assertEqual(html_node.value, "This is a text node")
    
	def test_bold(self):
		node_bold = TextNode("This is a text node in bold", TextType.BOLD)
		html_node_bold = text_node_to_html_node(node_bold)
		self.assertEqual(html_node_bold.tag, "b")
		self.assertEqual(html_node_bold.value, "This is a text node in bold")

	def test_italic(self):
		node_italic = TextNode("This is a text node in italic", TextType.ITALIC)
		html_node_italic = text_node_to_html_node(node_italic)
		self.assertEqual(html_node_italic.tag, "i")
		self.assertEqual(html_node_italic.value, "This is a text node in italic") 

	def test_code(self):
		node_code = TextNode("some code", TextType.CODE)
		html_node_code = text_node_to_html_node(node_code)
		self.assertEqual(html_node_code.tag, "code")      
		self.assertEqual(html_node_code.value,"some code")

	def test_link(self):
		node_link = TextNode("anchor text",TextType.LINK,"https://www.boot.dev")
		html_node_link = text_node_to_html_node(node_link)
		self.assertEqual(html_node_link.tag, "a")
		self.assertEqual(html_node_link.value, "anchor text")
		self.assertEqual(html_node_link.props, {"href":"https://www.boot.dev"})

	def test_image(self):
		node_image = TextNode("alt text", TextType.IMAGE,"src/image1.png")
		html_node_image = text_node_to_html_node(node_image)
		self.assertEqual(html_node_image.tag,"img") 
		self.assertEqual(html_node_image.value,"") 
		self.assertEqual(html_node_image.props,{"src": "src/image1.png", "alt": "alt text"}) 

	def test_raises(self):
		node = TextNode("some text","type underscore")
		with self.assertRaises(ValueError):
			html_node = text_node_to_html_node(node)


if __name__ == "__main__":
	unittest.main()
