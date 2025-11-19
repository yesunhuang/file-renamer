import os
import json
from pathlib import Path

class ConfigManager:
    def __init__(self):
        self.config_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'config')
        self.config_file = os.path.join(self.config_dir, 'settings.json')
        self.ensure_config_exists()

    def ensure_config_exists(self):
        """Ensure the config directory and file exist."""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
        
        if not os.path.exists(self.config_file):
            default_settings = {
                "api_keys": {
                    "gemini": "",
                    "openai": ""
                },
                "last_provider": "gemini",
                "selected_models": {
                    "gemini": "gemini-1.5-flash",
                    "openai": "gpt-3.5-turbo"
                },
                "theme": "light"
            }
            self.save_config(default_settings)

    def load_config(self):
        """Load configuration from file."""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return {}

    def save_config(self, config):
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False

    def get_api_key(self, provider):
        """Get API key for a specific provider."""
        config = self.load_config()
        return config.get("api_keys", {}).get(provider, "")

    def set_api_key(self, provider, key):
        """Set API key for a specific provider."""
        config = self.load_config()
        if "api_keys" not in config:
            config["api_keys"] = {}
        config["api_keys"][provider] = key
        return self.save_config(config)

    def get_model(self, provider):
        """Get selected model for a specific provider."""
        config = self.load_config()
        return config.get("selected_models", {}).get(provider, "")

    def set_model(self, provider, model):
        """Set selected model for a specific provider."""
        config = self.load_config()
        if "selected_models" not in config:
            config["selected_models"] = {}
        config["selected_models"][provider] = model
        return self.save_config(config)
