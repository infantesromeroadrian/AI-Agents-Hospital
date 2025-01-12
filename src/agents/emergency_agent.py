from typing import Dict
from src.core.base_agent import BaseAgent

class EmergencyAgent(BaseAgent):
    def _get_system_prompt(self) -> str:
        return """
        Eres un coordinador de sala de emergencias experto. DEBES responder ÚNICAMENTE con un JSON válido...
        """

    def manage_emergency(self, emergency_data: Dict, location: str = None) -> Dict:
        return self._make_llm_call(f"Coordina la emergencia: {emergency_data}") 