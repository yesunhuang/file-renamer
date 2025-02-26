import unittest, os
from src.file_operations import rename_files
from src.label_extractor import extract_label_from_name

class TestFileOperations(unittest.TestCase):

    def setUp(self):
        # Setup code to create test files and folders
        self.test_files = ['test_file_1.txt', 'test_file_2.txt']
        for file in self.test_files:
            with open(file, 'w') as f:
                f.write('This is a test file.')

    def tearDown(self):
        # Cleanup code to remove test files
        for file in self.test_files:
            try:
                os.remove(file)
            except FileNotFoundError:
                pass

    def test_rename_files(self):
        new_prefix = 'renamed_'
        renamed_files = rename_files(self.test_files, new_prefix)
        
        # Verify that the old files no longer exist
        for file in self.test_files:
            self.assertFalse(os.path.exists(file))
        
        # Verify that the new files exist
        for new_path in renamed_files:
            self.assertTrue(os.path.exists(new_path))

    def test_extract_label_from_name(self):
        file_name = 'example_label_file.txt'
        expected_label = 'example_label'
        self.assertEqual(extract_label_from_name(file_name), expected_label)

if __name__ == '__main__':
    unittest.main()