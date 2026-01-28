import requests
import json
import os

class AIRenamer:
    AVAILABLE_MODELS = {
        "gemini": ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.0-pro"],
        "openai": ["gpt-3.5-turbo", "gpt-4", "gpt-4o"]
    }

    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.cached_models = {}

    def get_available_models(self, provider):
        """
        Get list of available models for the provider.
        First tries to fetch from API, falls back to hardcoded list.
        """
        api_key = self.config_manager.get_api_key(provider)
        if not api_key:
            return self.AVAILABLE_MODELS.get(provider, [])
            
        # Check cache first (could add expiration later, but for now per-session is fine)
        if provider in self.cached_models:
            return self.cached_models[provider]

        try:
            if provider == 'gemini':
                models = self._fetch_gemini_models(api_key)
            elif provider == 'openai':
                models = self._fetch_openai_models(api_key)
            else:
                models = []
            
            if models:
                self.cached_models[provider] = models
                return models
        except Exception as e:
            print(f"Error fetching models for {provider}: {e}")
            
        return self.AVAILABLE_MODELS.get(provider, [])

    def _fetch_gemini_models(self, api_key):
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            models = []
            if 'models' in data:
                for m in data['models']:
                    name = m['name'].replace('models/', '')
                    # Filter for models that support generateContent and are likely chat models
                    if 'generateContent' in m.get('supportedGenerationMethods', []) and 'gemini' in name:
                        models.append(name)
            return sorted(models, reverse=True)
        except Exception as e:
            print(f"Failed to fetch Gemini models: {e}")
            return []

    def _fetch_openai_models(self, api_key):
        url = "https://api.openai.com/v1/models"
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            models = []
            if 'data' in data:
                for m in data['data']:
                    id = m['id']
                    # Filter for likely chat models
                    if id.startswith("gpt-") and "instruct" not in id and "realtime" not in id and "audio" not in id:
                         models.append(id)
            return sorted(models, reverse=True)
        except Exception as e:
            print(f"Failed to fetch OpenAI models: {e}")
            return []

    def construct_prompt(self, files, user_prompt):
        """
        Construct the system and full prompt for preview or execution.
        
        Returns:
            tuple: (system_instruction, full_prompt)
        """
        # Prepare the file list string
        file_list_str = "\n".join([os.path.basename(f) for f in files])
        
        # Construct the system/full prompt
        system_instruction = (
            "You are a file and folder renaming assistant. I will provide a list of filenames/foldernames and a user instruction. "
            "You must return a JSON object where keys are the original names and values are the new names. "
            "Do not include any markdown formatting or explanation, just the raw JSON string. "
            "If a file or folder should not be renamed, use the original name as the value."
        )
        
        full_prompt = (
            f"User Instruction: {user_prompt}\n\n"
            f"Items to rename:\n{file_list_str}\n\n"
            "Return ONLY valid JSON mapping old names to new names."
        )
        return system_instruction, full_prompt

    def get_rename_suggestions(self, files, user_prompt, provider, model=None):
        """
        Get rename suggestions from AI.
        
        Args:
            files (list): List of file/folder paths or names.
            user_prompt (str): User's instruction for renaming.
            provider (str): 'gemini' or 'openai'.
            model (str, optional): Specific model to use.
            
        Returns:
            list: List of tuples (old_name, new_name).
        """
        api_key = self.config_manager.get_api_key(provider)
        if not api_key:
            raise ValueError(f"API Key for {provider} is missing.")

        system_instruction, full_prompt = self.construct_prompt(files, user_prompt)

        try:
            if provider == 'gemini':
                return self._call_gemini(api_key, system_instruction, full_prompt, files, model)
            elif provider == 'openai':
                return self._call_openai(api_key, system_instruction, full_prompt, files, model)
            else:
                raise ValueError(f"Unsupported provider: {provider}")
        except Exception as e:
            print(f"AI Error: {e}")
            raise e

    def _call_gemini(self, api_key, system_instruction, user_message, files, model=None):
        model = model or "gemini-1.5-flash"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [{
                "parts": [{"text": system_instruction + "\n\n" + user_message}]
            }]
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        try:
            text_content = result['candidates'][0]['content']['parts'][0]['text']
            return self._parse_json_response(text_content, files)
        except (KeyError, IndexError) as e:
            raise ValueError(f"Unexpected response structure from Gemini: {result}")

    def _call_openai(self, api_key, system_instruction, user_message, files, model=None):
        model = model or "gpt-3.5-turbo"
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.7
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        try:
            text_content = result['choices'][0]['message']['content']
            return self._parse_json_response(text_content, files)
        except (KeyError, IndexError) as e:
            raise ValueError(f"Unexpected response structure from OpenAI: {result}")

    def _parse_json_response(self, text_content, original_files):
        """Parses the JSON response and maps it back to the original file paths."""
        # Clean up markdown code blocks if present
        text_content = text_content.strip()
        if text_content.startswith("```json"):
            text_content = text_content[7:]
        if text_content.startswith("```"):
            text_content = text_content[3:]
        if text_content.endswith("```"):
            text_content = text_content[:-3]
        
        try:
            mapping = json.loads(text_content)
        except json.JSONDecodeError:
            # Fallback: try to find JSON-like structure
            start = text_content.find('{')
            end = text_content.rfind('}') + 1
            if start != -1 and end != -1:
                try:
                    mapping = json.loads(text_content[start:end])
                except:
                    raise ValueError(f"Failed to parse JSON from AI response: {text_content}")
            else:
                raise ValueError(f"Failed to parse JSON from AI response: {text_content}")

        suggestions = []
        # Create a lookup for basenames to full paths
        basename_map = {os.path.basename(f): f for f in original_files}
        
        for old_name, new_name in mapping.items():
            if old_name in basename_map:
                suggestions.append((basename_map[old_name], new_name))
            else:
                # Handle case where AI might have slightly altered the old name or it's missing
                # For now just skip or log warning
                print(f"Warning: AI returned unknown file '{old_name}'")
                
        return suggestions
