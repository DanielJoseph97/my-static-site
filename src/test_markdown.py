import unittest
from inline_markdown import *
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

class TestSplitMarkdown(unittest.TestCase):
	def test_split_images(self):
		node = TextNode(
			"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
		TextType.TEXT,)
		new_nodes = split_nodes_image([node])
		self.assertListEqual(
			[
				TextNode("This is text with an ", TextType.TEXT),
				TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
				TextNode(" and another ", TextType.TEXT),
				TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
				],
				new_nodes,)

	def test_split_image_single(self):
		node = TextNode("![image](https://www.example.COM/IMAGE.PNG)",TextType.TEXT,
        )
		new_nodes = split_nodes_image([node])
		self.assertListEqual(
			[TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,)

	def test_split_images(self):
		node = TextNode(
			"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
			TextType.TEXT,
		)
		new_nodes = split_nodes_image([node])
		self.assertListEqual(
			[
				TextNode("This is text with an ", TextType.TEXT),
				TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
				TextNode(" and another ", TextType.TEXT),
				TextNode(
					"second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
				),
			],
			new_nodes,
		)

	def test_split_links(self):
		node = TextNode(
			"This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
			TextType.TEXT,
		)
		new_nodes = split_nodes_link([node])
		self.assertListEqual(
			[
				TextNode("This is text with a ", TextType.TEXT),
				TextNode("link", TextType.LINK, "https://boot.dev"),
				TextNode(" and ", TextType.TEXT),
				TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
				TextNode(" with text that follows", TextType.TEXT),
			],
			new_nodes,
		)

class TestRawTextToMarkdown(unittest.TestCase):
	def test_raw_text_to_markdown(self):
		raw_text = "This is **text** with an _italic_ word an" \
		"d a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) an" \
		"d a [link](https://boot.dev)"
		text_nodes = text_to_textnodes(raw_text)
		self.assertListEqual(
			[
			TextNode("This is ", TextType.TEXT),
			TextNode("text", TextType.BOLD),
			TextNode(" with an ", TextType.TEXT),
			TextNode("italic", TextType.ITALIC),
			TextNode(" word and a ", TextType.TEXT),
			TextNode("code block", TextType.CODE),
			TextNode(" and an ", TextType.TEXT),
			TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
			TextNode(" and a ", TextType.TEXT),
			TextNode("link", TextType.LINK, "https://boot.dev"),
		], text_nodes
		)

if __name__ == "__main__":
	unittest.main()
