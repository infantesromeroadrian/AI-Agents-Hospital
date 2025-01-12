from typing import Dict, List
from src.core.base_agent import BaseAgent

class PharmacistAgent(BaseAgent):
    def _get_system_prompt(self) -> str:
        return """
        Eres un farmacéutico experto. DEBES responder ÚNICAMENTE con un JSON válido...
        """

    def review_prescription(self, patient_id: str, prescriptions: List[str], patient_data: str) -> Dict:
        return self._make_llm_call(f"Revisa las prescripciones: {prescriptions}") 