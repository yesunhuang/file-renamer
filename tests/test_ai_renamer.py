import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ai_renamer import AIRenamer
from src.config_manager import ConfigManager

class TestAIRenamer(unittest.TestCase):
    def setUp(self):
        self.mock_config = MagicMock(spec=ConfigManager)
        self.mock_config.get_api_key.return_value = "fake_key"
        self.renamer = AIRenamer(self.mock_config)

    def test_parse_json_response_simple(self):
        files = ["/path/to/file1.txt", "/path/to/file2.txt"]
        json_response = '{"file1.txt": "new1.txt", "file2.txt": "new2.txt"}'
        
        suggestions = self.renamer._parse_json_response(json_response, files)
        
        expected = [("/path/to/file1.txt", "new1.txt"), ("/path/to/file2.txt", "new2.txt")]
        self.assertEqual(suggestions, expected)

    def test_parse_json_response_markdown(self):
        files = ["/path/to/photo.jpg"]
        json_response = '```json\n{"photo.jpg": "vacation.jpg"}\n```'
        
        suggestions = self.renamer._parse_json_response(json_response, files)
        
        expected = [("/path/to/photo.jpg", "vacation.jpg")]
        self.assertEqual(suggestions, expected)

    @patch('requests.post')
    def test_call_gemini(self, mock_post):
        # Mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "candidates": [{
                "content": {
                    "parts": [{"text": '{"test.txt": "renamed.txt"}'}]
                }
            }]
        }
        mock_post.return_value = mock_response
        
        files = ["/path/to/test.txt"]
        suggestions = self.renamer.get_rename_suggestions(files, "rename it", "gemini")
        
        self.assertEqual(suggestions, [("/path/to/test.txt", "renamed.txt")])

if __name__ == '__main__':
    unittest.main()
