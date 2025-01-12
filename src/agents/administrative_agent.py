from typing import Dict
from src.core.base_agent import BaseAgent

class AdministrativeAgent(BaseAgent):
    def _get_system_prompt(self) -> str:
        return """
        Eres un administrador hospitalario experto. DEBES responder ÚNICAMENTE con un JSON válido...
        """

    def manage_admission(self, patient_id: str, medical_data: Dict, insurance_info: str = None) -> Dict:
        return self._make_llm_call(f"Gestiona la admisión del paciente: {medical_data}") 