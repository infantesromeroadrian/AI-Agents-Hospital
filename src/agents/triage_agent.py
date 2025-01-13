from typing import Dict
from src.core.base_agent import BaseAgent

class TriageAgent(BaseAgent):
    """Agent responsible for initial patient assessment and triage"""
    
    def _get_system_prompt(self) -> str:
        return """Eres un agente de triaje médico experto. Tu tarea es evaluar los síntomas del paciente y determinar:

1. Nivel de urgencia (1-5):
   - 1: Resucitación (atención inmediata)
   - 2: Emergencia (muy urgente, minutos)
   - 3: Urgente (hasta 1 hora)
   - 4: Menos urgente (hasta 2 horas)
   - 5: No urgente (hasta 4 horas)

2. Departamento médico apropiado (uno de los siguientes):
   - Medicina General
   - Urgencias
   - Pediatría
   - Cardiología
   - Gastroenterología
   - Traumatología
   - Neurología

3. Acciones inmediatas y evaluación

Responde ÚNICAMENTE en formato JSON con esta estructura exacta:
{
    "urgency_level": int,
    "department": string,
    "immediate_actions": [string],
    "assessment": string,
    "vital_signs_needed": [string]
}"""

    def evaluate_patient(self, symptoms: str) -> Dict:
        """Evaluate patient symptoms and determine urgency"""
        prompt = f"""Por favor, evalúa los siguientes síntomas del paciente y proporciona una evaluación detallada siguiendo el formato especificado:

Síntomas: {symptoms}

Recuerda:
- Asignar un nivel de urgencia del 1 al 5
- Especificar el departamento más apropiado
- Listar acciones inmediatas necesarias
- Proporcionar una evaluación clara
- Indicar signos vitales que deben monitorearse"""
        
        return self._make_llm_call(prompt) 