import unittest
from markdown_blocks import BlockType, markdown_to_blocks, block_to_block_type

class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_headings(self):
        input1 = "# This is a heading"
        input2 = "## This is a heading"
        input3 = "### This is a heading"
        input4 = "#### This is a heading"
        input5 = "##### This is a heading"
        input6 = "###### This is a heading"
        block_1 = block_to_block_type(input1)
        block_2 = block_to_block_type(input2)
        block_3 = block_to_block_type(input3)
        block_4 = block_to_block_type(input4)
        block_5 = block_to_block_type(input5)
        block_6 = block_to_block_type(input6)
        self.assertEqual(block_1, BlockType.HEADING)
        self.assertEqual(block_2, BlockType.HEADING)
        self.assertEqual(block_3, BlockType.HEADING)
        self.assertEqual(block_4, BlockType.HEADING)
        self.assertEqual(block_5, BlockType.HEADING)
        self.assertEqual(block_6, BlockType.HEADING)
    
    def test_code(self):
        input = "```\nsome code\n```"
        block = block_to_block_type(input)
        self.assertEqual(block, BlockType.CODE)
    
    def test_quote(self):
        input = "> To be\n> or not to be"
        block = block_to_block_type(input)
        self.assertEqual(block,BlockType.QUOTE)
    
    def test_unordered_list(self):
        input = "- some stuff\n- some more stuff\n- even more stuff"
        block = block_to_block_type(input)
        self.assertEqual(block,BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        input = "1. some stuff\n2. some more stuff\n3. even more stuff"
        block = block_to_block_type(input)
        self.assertEqual(block,BlockType.ORDERED_LIST)
    
    def test_paragraph(self):
        input = "Some text that shoul" \
        "d fall in between all scenari" \
        "os\n- such that no single bloc" \
        "k type is detected\n1. so hopeful" \
        "ly\nthis works as intended\n> A" \
        "s they say\ncan only test somethi" \
        "ng\n```by trying it out```\nso her" \
        "e's an attempt"
        block = block_to_block_type(input)
        self.assertEqual(block, BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()