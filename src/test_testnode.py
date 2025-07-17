import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from markdown_to_textnode import split_nodes_delimiter

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

class TestInlineMarkdown(unittest.TestCase):
	def test_delim_code(self):
		node = TextNode("This is text with a `code block` word", TextType.TEXT)
		new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
		self.assertListEqual(
			[
				TextNode("This is text with a ", TextType.TEXT),
				TextNode("code block", TextType.CODE),
				TextNode(" word", TextType.TEXT)
			], 
			new_nodes,
		)	

	def test_delim_bold(self):
		node = TextNode("This is text with a **bold statement** word", TextType.TEXT)
		new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
		self.assertListEqual(
			[
				TextNode("This is text with a ", TextType.TEXT),
				TextNode("bold statement", TextType.BOLD),
				TextNode(" word", TextType.TEXT)
			], 
			new_nodes,
		)

	def test_delim_italic(self):
		node = TextNode("This is text with a _italic statement_ word", TextType.TEXT)
		new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
		self.assertListEqual(
			[
				TextNode("This is text with a ", TextType.TEXT),
				TextNode("italic statement", TextType.ITALIC),
				TextNode(" word", TextType.TEXT)
			], 
			new_nodes,
		)

	def test_delim_bold_multiword(self):
		node = TextNode("This is a text with **Bold1 text** and **Bold2 text** as well", TextType.TEXT)
		new_nodes = split_nodes_delimiter([node], "**",TextType.BOLD)
		self.assertListEqual(
			[
				TextNode("This is a text with ", TextType.TEXT),
				TextNode("Bold1 text", TextType.BOLD),
				TextNode(" and ", TextType.TEXT),
				TextNode("Bold2 text",TextType.BOLD),
				TextNode(" as well", TextType.TEXT),
			],
			new_nodes,
		)
	
	def test_delim_bold_and_italic(self):
		node = TextNode("**bold** and _italic_", TextType.TEXT)
		new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
		new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
		self.assertListEqual(
			[
				TextNode("bold", TextType.BOLD),
				TextNode(" and ", TextType.TEXT),
				TextNode("italic", TextType.ITALIC),
			],
			new_nodes,
		)
	
	def test_no_delim(self):
		node = TextNode("This is text with no delimiters", TextType.TEXT)
		new_node = split_nodes_delimiter([node], "**",TextType.BOLD)
		self.assertEqual(new_node[0],TextNode("This is text with no delimiters", TextType.TEXT))

	def test_invalid_delim_raises(self):
		node = TextNode("This is a text with ``code block missing",TextType.TEXT)
		with self.assertRaises(Exception):
			new_node = split_nodes_delimiter([node],"``",TextType.CODE)

		
if __name__ == "__main__":
	unittest.main()
