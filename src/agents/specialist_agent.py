from typing import Dict
from src.core.base_agent import BaseAgent

class SpecialistAgent(BaseAgent):
    def _get_system_prompt(self) -> str:
        return """
        Eres un médico especialista experto. DEBES responder ÚNICAMENTE con un JSON válido que contenga los siguientes campos:
        {
            "diagnosis": "diagnóstico preliminar",
            "confidence_level": (número del 1 al 100),
            "required_tests": ["test 1", "test 2", ...],
            "treatment_plan": ["paso 1", "paso 2", ...],
            "prescriptions": ["medicamento 1", "medicamento 2", ...],
            "follow_up": "tiempo recomendado para siguiente revisión",
            "warnings": ["advertencia 1", "advertencia 2", ...],
            "specialist_notes": "notas adicionales importantes"
        }

        Asegúrate de:
        1. Proporcionar un diagnóstico basado en la evidencia
        2. Sugerir pruebas relevantes
        3. Crear un plan de tratamiento específico
        4. Incluir advertencias y contraindicaciones importantes
        """

    def evaluate_case(self, patient_data: str, specialty: str) -> Dict:
        prompt = f"""
        Como especialista en {specialty}, evalúa el siguiente caso:
        {patient_data}
        
        Proporciona una evaluación detallada y plan de tratamiento.
        """
        return self._make_llm_call(prompt) 