import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.ai_renamer import AIRenamer
from src.config_manager import ConfigManager

class TestModelFetching(unittest.TestCase):
    def setUp(self):
        self.mock_config = MagicMock(spec=ConfigManager)
        self.renamer = AIRenamer(self.mock_config)

    @patch('src.ai_renamer.requests.get')
    def test_fetch_gemini_models_success(self, mock_get):
        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "models": [
                {"name": "models/gemini-pro", "supportedGenerationMethods": ["generateContent"]},
                {"name": "models/gemini-1.5-flash", "supportedGenerationMethods": ["generateContent"]},
                {"name": "models/embedding-001", "supportedGenerationMethods": ["embedContent"]}, # Should be filtered out
                {"name": "models/other-model", "supportedGenerationMethods": ["generateContent"]} # Should be filtered out (no 'gemini')
            ]
        }
        mock_get.return_value = mock_response
        self.mock_config.get_api_key.return_value = "fake_key"

        models = self.renamer.get_available_models("gemini")
        
        self.assertIn("gemini-pro", models)
        self.assertIn("gemini-1.5-flash", models)
        self.assertNotIn("embedding-001", models)
        self.assertNotIn("other-model", models)
        
    @patch('src.ai_renamer.requests.get')
    def test_fetch_openai_models_success(self, mock_get):
        # Mock API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": [
                {"id": "gpt-4"},
                {"id": "gpt-3.5-turbo"},
                {"id": "gpt-4-0314"},
                {"id": "davinci-instruct-beta"}, # Should be filtered out (instruct)
                {"id": "whisper-1"} # Should be filtered out (no gpt-)
            ]
        }
        mock_get.return_value = mock_response
        self.mock_config.get_api_key.return_value = "fake_key"

        models = self.renamer.get_available_models("openai")
        
        self.assertIn("gpt-4", models)
        self.assertIn("gpt-3.5-turbo", models)
        self.assertNotIn("whisper-1", models)

    @patch('src.ai_renamer.requests.get')
    def test_fallback_behavior(self, mock_get):
        # Simulate API failure
        mock_get.side_effect = Exception("API Error")
        self.mock_config.get_api_key.return_value = "fake_key"

        # Should return default list
        gemini_models = self.renamer.get_available_models("gemini")
        self.assertEqual(gemini_models, self.renamer.AVAILABLE_MODELS["gemini"])
        
        openai_models = self.renamer.get_available_models("openai")
        self.assertEqual(openai_models, self.renamer.AVAILABLE_MODELS["openai"])

    def test_no_api_key(self):
        self.mock_config.get_api_key.return_value = ""
        
        # Should return default list without calling API
        models = self.renamer.get_available_models("gemini")
        self.assertEqual(models, self.renamer.AVAILABLE_MODELS["gemini"])

if __name__ == '__main__':
    unittest.main()
