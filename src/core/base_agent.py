from abc import ABC, abstractmethod
from typing import Dict, Any
from datetime import datetime
import json

class BaseAgent(ABC):
    """Base class for all hospital agents"""
    
    def __init__(self, client):
        self.client = client
        self.system_prompt = self._get_system_prompt()
    
    @abstractmethod
    def _get_system_prompt(self) -> str:
        """Return the system prompt for this agent"""
        pass
    
    def _make_llm_call(self, prompt: str, temperature: float = 0.2) -> Dict:
        """Make a call to the LLM"""
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile",
                temperature=temperature,
                max_tokens=1024,
                response_format={"type": "json_object"}
            )
            
            # Parse the JSON response
            try:
                return json.loads(response.choices[0].message.content)
            except json.JSONDecodeError as e:
                return {
                    "error": "Error parsing JSON response",
                    "raw_response": response.choices[0].message.content,
                    "details": str(e),
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            return {
                "error": f"Error in LLM call: {str(e)}",
                "timestamp": datetime.now().isoformat()
            } 