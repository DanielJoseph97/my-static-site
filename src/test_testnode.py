import unittest

from textnode import TextNode, TextType

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
	
	def test_noteq_url(self):
		node = TextNode("Type1", TextType.TEXT)
		node2 = TextNode("Type2", TextType.TEXT, "https://boot.dev")
		self.assertNotEqual(node, node2)

	def test_noteq_different_url(self):
		node = TextNode("Type1", TextType.TEXT, "https://wikipedia.org")
		node2 = TextNode("Type1", TextType.TEXT, "https://boot.dev")
		self.assertNotEqual(node, node2)

	def test_eq_url(self):
		node = TextNode("Some text", TextType.TEXT, url=None)
		node2 = TextNode("Some text", TextType.TEXT, url=None)
		self.assertEqual(node, node2)


if __name__ == "__main__":
	unittest.main()
