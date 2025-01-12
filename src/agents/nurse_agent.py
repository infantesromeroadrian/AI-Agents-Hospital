from typing import Dict
from src.core.base_agent import BaseAgent

class NurseAgent(BaseAgent):
    def _get_system_prompt(self) -> str:
        return """
        Eres un enfermero/a experto/a. DEBES responder ÚNICAMENTE con un JSON válido...
        """

    def monitor_patient(self, patient_id: str, patient_data: str, care_plan: Dict) -> Dict:
        return self._make_llm_call(f"Monitorea al paciente: {patient_data}") 