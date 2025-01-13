from abc import ABC, abstractmethod
from typing import Dict
from datetime import datetime
import json
import requests
from src.config.settings import MODEL_NAME

class BaseAgent(ABC):
    """Base class for all hospital agents"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    @abstractmethod
    def _get_system_prompt(self) -> str:
        """Return the system prompt for this agent"""
        pass
    
    def _make_llm_call(self, prompt: str) -> Dict:
        """Make API call to Groq"""
        try:
            data = {
                "model": MODEL_NAME,
                "messages": [
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.2,
                "max_tokens": 1024,
                "response_format": {"type": "json_object"}
            }
            
            print(f"Making API call with data: {data}")
            
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=data,
                timeout=60
            )
            
            print(f"Response status: {response.status_code}")
            print(f"Response text: {response.text}")
            
            if response.status_code != 200:
                return {
                    "error": f"API Error: {response.status_code} - {response.text}",
                    "timestamp": datetime.now().isoformat()
                }
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                print(f"JSON Decode Error. Raw content: {content}")
                return {
                    "error": "Invalid JSON response",
                    "raw_response": content,
                    "timestamp": datetime.now().isoformat()
                }
            
        except Exception as e:
            error_msg = f"Error in LLM call: {str(e)}"
            print(error_msg)
            return {
                "error": error_msg,
                "timestamp": datetime.now().isoformat()
            } 