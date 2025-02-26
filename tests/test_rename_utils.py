import unittest
from src.rename_utils import generate_new_name, apply_prefix_format

class TestRenameUtils(unittest.TestCase):

    def test_generate_new_name(self):
        # Test case for generating new names
        original_name = "example_file.txt"
        prefix = "new_"
        expected_name = "new_example_file.txt"
        self.assertEqual(generate_new_name(original_name, prefix, None), expected_name)

    def test_apply_prefix_format(self):
        # Test case for applying prefix format
        original_name = "document.pdf"
        prefix_format = "doc_{}"
        expected_name = "doc_document.pdf"
        self.assertEqual(apply_prefix_format(original_name, prefix_format), expected_name)

    def test_generate_new_name_with_empty_prefix(self):
        # Test case for generating new name with empty prefix
        original_name = "image.png"
        prefix = ""
        expected_name = "image.png"
        self.assertEqual(generate_new_name(original_name, prefix, None), expected_name)

    def test_apply_prefix_format_with_no_format(self):
        # Test case for applying prefix format with no format
        original_name = "report.docx"
        prefix_format = ""
        expected_name = "report.docx"
        self.assertEqual(apply_prefix_format(original_name, prefix_format), expected_name)

if __name__ == '__main__':
    unittest.main()