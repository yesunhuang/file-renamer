import os
import sys
import shutil
import unittest
from unittest.mock import patch, MagicMock

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.main import run_ai_renaming_operation

class TestFolderRenaming(unittest.TestCase):
    def setUp(self):
        self.test_dir = os.path.join(os.path.dirname(__file__), "temp_test_folder_renaming")
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        os.makedirs(self.test_dir)
        
        # Create a file and a folder
        self.test_file = os.path.join(self.test_dir, "test_file.txt")
        with open(self.test_file, "w") as f:
            f.write("content")
            
        self.test_folder = os.path.join(self.test_dir, "test_folder")
        os.makedirs(self.test_folder)
        
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    @patch('src.main.get_user_input')
    @patch('src.ai_renamer.AIRenamer')
    @patch('src.config_manager.ConfigManager')
    @patch('src.main.confirm_action')
    def test_folder_renaming_flow(self, mock_confirm, mock_config_manager, mock_ai_renamer_class, mock_input):
        # Setup mocks
        mock_confirm.return_value = True
        
        # Mock ConfigManager
        mock_config = MagicMock()
        mock_config.get_api_key.return_value = "fake_key"
        mock_config_manager.return_value = mock_config
        
        # Mock AIRenamer
        mock_ai = MagicMock()
        mock_ai_renamer_class.return_value = mock_ai
        
        # Mock suggestions: Rename file to file_renamed.txt, folder to folder_renamed
        mock_ai.get_rename_suggestions.return_value = [
            (self.test_file, "file_renamed.txt"),
            (self.test_folder, "folder_renamed")
        ]
        
        # Mock inputs
        # 1. Directory path
        # 2. Prompt
        # 3. Provider choice (1 for Gemini)
        # 4. Include folders? (y)
        mock_input.side_effect = [
            self.test_dir,
            "rename everything",
            "1",
            "y"
        ]
        
        # Run the operation
        run_ai_renaming_operation()
        
        # Verify results
        new_file_path = os.path.join(self.test_dir, "file_renamed.txt")
        new_folder_path = os.path.join(self.test_dir, "folder_renamed")
        
        self.assertTrue(os.path.exists(new_file_path), "File should have been renamed")
        self.assertTrue(os.path.exists(new_folder_path), "Folder should have been renamed")
        self.assertFalse(os.path.exists(self.test_file), "Old file should not exist")
        self.assertFalse(os.path.exists(self.test_folder), "Old folder should not exist")
        
        # Verify AIRenamer was called with correct arguments
        # We can't easily check the 'files' argument exact content because order might vary, 
        # but we can check if it was called.
        mock_ai.get_rename_suggestions.assert_called_once()
        call_args = mock_ai.get_rename_suggestions.call_args
        self.assertEqual(call_args[0][1], "rename everything")
        self.assertEqual(call_args[0][2], "gemini")
        
        # Verify items passed to AI included the folder
        items_passed = call_args[0][0]
        self.assertIn(self.test_folder, items_passed)
        self.assertIn(self.test_file, items_passed)

if __name__ == '__main__':
    unittest.main()
