from typing import Dict
from src.core.base_agent import BaseAgent

class TriageAgent(BaseAgent):
    """Agent responsible for initial patient assessment and triage"""
    
    def _get_system_prompt(self) -> str:
        return """
        Eres un agente de triaje médico experto. DEBES responder ÚNICAMENTE con un JSON válido que contenga los siguientes campos:
        {
            "urgency_level": (número del 1 al 5),
            "department": "nombre del departamento",
            "immediate_actions": ["acción 1", "acción 2", ...],
            "reasoning": "explicación de la decisión"
        }

        Niveles de urgencia:
        1 - Resucitación (atención inmediata)
        2 - Emergencia (muy urgente, minutos)
        3 - Urgente (hasta 1 hora)
        4 - Menos urgente (hasta 2 horas)
        5 - No urgente (hasta 4 horas)
        """

    def evaluate_patient(self, symptoms: str) -> Dict:
        """
        Evalúa los síntomas del paciente y determina el nivel de urgencia
        """
        prompt = f"""
        Evalúa los siguientes síntomas y responde SOLO con un JSON válido:
        {symptoms}
        """
        
        return self._make_llm_call(prompt) 