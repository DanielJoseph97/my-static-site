import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType
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

class TestMarkdownRegex(unittest.TestCase):
	def test_extract_single_link(self):
		text = "This is text with a link [to boot dev](https://www.boot.dev)"
		matches = extract_markdown_links(text)
		self.assertListEqual(
			[
				("to boot dev", "https://www.boot.dev")
				], matches
			)

	def test_extract_multiple_links(self):
		text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
		matches = extract_markdown_links(text)
		self.assertListEqual(
			[
				("to boot dev", "https://www.boot.dev"), 
				("to youtube", "https://www.youtube.com/@bootdotdev")
				], matches
			)

	def test_no_links(self):
		text = "This is just plain text with no links"
		matches = extract_markdown_links(text)
		self.assertListEqual([], matches)

	def test_mixed_images_and_links(self):
		text = "Here's an image ![alt text](image.jpg) and a [link](https://example.com)"
		matches = extract_markdown_links(text)
		self.assertListEqual(
			[
				("link", "https://example.com")
				], 
				matches
			)

	def test_ignores_images(self):
		text = "This has an image ![not a link](image.jpg) but no links"
		matches = extract_markdown_links(text)
		self.assertListEqual([], matches)

if __name__ == "__main__":
	unittest.main()
