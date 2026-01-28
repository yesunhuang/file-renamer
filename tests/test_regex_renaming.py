import sys
import os
import unittest

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.rename_utils import apply_regex_rename

class TestRegexRenaming(unittest.TestCase):
    def test_basic_regex_replace(self):
        name = "test_file_123.txt"
        pattern = r"test_file_(\d+)"
        replacement = r"image_\1"
        new_name = apply_regex_rename(name, pattern, replacement)
        self.assertEqual(new_name, "image_123.txt")

    def test_regex_group_swapping(self):
        name = "John_Doe.txt"
        pattern = r"(\w+)_(\w+)"
        replacement = r"\2_\1"
        new_name = apply_regex_rename(name, pattern, replacement)
        self.assertEqual(new_name, "Doe_John.txt")

    def test_regex_no_match(self):
        name = "simple_file.txt"
        pattern = r"\d+"
        replacement = "X"
        new_name = apply_regex_rename(name, pattern, replacement)
        self.assertEqual(new_name, "simple_file.txt")

    def test_invalid_regex(self):
        name = "test.txt"
        pattern = r"["  # Invalid regex
        replacement = "ops"
        new_name = apply_regex_rename(name, pattern, replacement)
        self.assertEqual(new_name, "test.txt") # Should return original on error

    def test_empty_pattern(self):
        name = "test.txt"
        pattern = ""
        replacement = "foo"
        new_name = apply_regex_rename(name, pattern, replacement)
        self.assertEqual(new_name, "test.txt")

if __name__ == '__main__':
    unittest.main()
